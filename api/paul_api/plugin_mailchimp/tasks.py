from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

from api.models import Table
from plugin_mailchimp import utils
from plugin_mailchimp.models import (
    Task,
    TaskResult,
    Settings as MailchimpSettings,
)
from plugin_mailchimp.table_fields import AUDIENCE_MEMBERS_FIELDS


def run_contacts_to_mailchimp(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        # TODO: We should delete the django q tasks for deleted mailchimp tasks
        raise Exception("The contacts upload task with id {} does not exist anymore".format(task_id))

    if request_user_id:
        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if not user:
        user, _ = User.objects.get_or_create(username='paul-sync')

    # TODO: Work in progress...
    task_result = TaskResult.objects.create(
        user=user,
        task=task,
        success=False,
        status = TaskResult.FINISHED,
        stats = {'details': ['This function is not yet implemented.']}
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
        user, _ = User.objects.get_or_create(username='paul-sync')

    settings = MailchimpSettings.objects.latest()
    task_result = TaskResult.objects.create(
        user=user,
        task=task
    )

    try:
        success, stats = utils.retrieve_lists_data(settings.key)
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
        user, _ = User.objects.get_or_create(username='paul-sync')

    token, _ = Token.objects.get_or_create(user=user)
    settings = MailchimpSettings.objects.latest()

    task_result = TaskResult.objects.create(
        user=user,
        task=task)

    filtered_view = task.segmentation_task.filtered_view
    primary_table = filtered_view.primary_table

    audience_members_table = Table.objects.filter(table_type=Table.TYPE_CONTACTS).last()

    if not audience_members_table:
        success = False
        stats['errors'] += 1
        stats['details'].append('Audience tables does not exist')
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
            lists_users = utils.get_emails_from_filtered_view(token, filtered_view, settings)
            success, stats = utils.add_list_to_segment(
                    settings,
                    lists_users,
                    task.segmentation_task.tag)

    task_result.success = success
    task_result.stats = stats
    task_result.status = TaskResult.FINISHED
    task_result.save()

    return task_result.id, task_result.success
