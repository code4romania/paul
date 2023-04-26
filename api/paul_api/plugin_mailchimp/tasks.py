from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError
from rest_framework.authtoken.models import Token

from api.models import Table
from plugin_mailchimp import utils
from plugin_mailchimp.models import (
    Task,
    TaskResult,
)
from plugin_mailchimp.table_fields import AUDIENCE_MEMBERS_FIELDS


def run_contacts_to_mailchimp(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Exception("The contacts upload task with id {} does not exist anymore".format(task_id))

    if request_user_id:
        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if not user:
        user, _ = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

    success = True
    stats = {
        "errors": 0,
        "skipped": 0,
        "updated": 0,
        "details": []
    }

    client = MailChimp(settings.MAILCHIMP_KEY)
    contacts_table = Table.objects.filter(table_type=Table.TYPE_CONTACTS).last()

    if not contacts_table:
        success = False
        stats["errors"] += 1
        stats["details"].append(_("Contacts' table does not exist"))
    else:
        all_contacts = utils.get_all_contacts(contacts_table)
        for contact in all_contacts:
            if not "audience_id" in contact.keys():
                print("skipping: ", contact)
                stats["skipped"] += 1
                continue

            try:
                response = client.lists.members.create_or_update(
                    contact.get("audience_id"), 
                    contact.get("email_address", ""),  # "subscriber_hash" also accepts the email address
                    {
                        "email_address": contact.get("email_address", ""),
                        # "merge_fields": contact.get("merge_fields", ""),  # TODO
                        "status_if_new": "unsubscribed",
                    })
            except MailChimpError:
                print("error: ", contact)
                stats["errors"] += 1
            else:
                stats["updated"] += 1

    stats["details"].append("{} contacts created or updated".format(stats["updated"]))
    stats["details"].append("{} contacts skipped".format(stats["skipped"]))
    stats["details"].append("{} contacts failed to create or update".format(stats["errors"]))

    task_result = TaskResult.objects.create(
        user=user,
        task=task,
        success=success,
        status=TaskResult.FINISHED,
        stats=stats,
    )
    return task_result.id, task_result.success


def run_sync(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Exception("The sync task with id {} does not exist anymore".format(task_id))

    if request_user_id:
        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if not user:
        user, _ = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

    task_result = TaskResult.objects.create(
        user=user,
        task=task
    )

    try:
        success, stats = utils.retrieve_lists_data(MailChimp(settings.MAILCHIMP_KEY))
        task_result.success = success
        task_result.stats = stats
        task_result.status = TaskResult.FINISHED
    except Exception as e:
        task_result.success = False
        task_result.status = TaskResult.FINISHED
        task_result.stats = {
            'details': [str(e)]
        }

    stats_details = []
    if task_result.success:
        for table, table_stats in task_result.stats.items():
            for k, v in table_stats.items():
                stats_details.append('<b>{}</b> {} in <b>{}</b>'.format(v, k, table))
        task_result.stats['details'] = stats_details
    task_result.date_end = timezone.now()
    task_result.duration = task_result.date_end - task_result.date_start
    task_result.save()
    return task_result.id, task_result.success


def run_segmentation(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Exception("The segmentation task with id {} does not exist anymore".format(task_id))

    success = True
    stats = {
        'success': 0,
        'errors': 0,
        'details': []
    }

    if request_user_id:
        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if not user:
        user, _ = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

    token, _ = Token.objects.get_or_create(user=user)
    # settings = MailchimpSettings.objects.latest()

    task_result = TaskResult.objects.create(
        user=user,
        task=task)

    filtered_view = task.segmentation_task.filtered_view
    primary_table = filtered_view.primary_table

    audience_members_table = Table.objects.filter(table_type=Table.TYPE_CONTACTS).last()

    if not audience_members_table:
        success = False
        stats['errors'] += 1
        stats['details'].append("Contacts' table does not exist")
    else:
        if primary_table.table != audience_members_table:
            success = False
            stats['errors'] += 1
            stats['details'].append(
                '<b>{}</b> needs to be the primary table in <b>{}</b> filtered view'.format(
                    audience_members_table, filtered_view.name
                ))
        primary_table_fields =  primary_table.fields.values_list('name', flat=True)
        mandatory_fields = ['audience_id', 'id', 'email_address']
        for field in mandatory_fields:
            if field not in primary_table_fields:
                success = False
                stats['errors'] += 1
                stats['details'].append(
                    '<b>{}</b> field needs to be selected in the primary table in <b>{}</b> filtered view'.format(
                        AUDIENCE_MEMBERS_FIELDS[field]['display_name'], filtered_view.name
                    ))
        if success:
            lists_users = utils.get_emails_from_filtered_view(token, filtered_view)
            success, stats = utils.add_list_to_segment(
                    MailChimp(settings.MAILCHIMP_KEY),
                    lists_users,
                    task.segmentation_task.tag)

    task_result.success = success
    task_result.stats = stats
    task_result.status = TaskResult.FINISHED
    task_result.save()

    return task_result.id, task_result.success
