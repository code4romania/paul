from ast import literal_eval

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError
from rest_framework.authtoken.models import Token

from api.models import Table
from plugin_mailchimp import utils, table_fields
from plugin_mailchimp.models import Task, TaskResult


def run_contacts_to_mailchimp(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Exception(_("The contacts upload task with id {} does not exist anymore").format(task_id))

    if request_user_id:
        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if not user:
        user, created = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

    success = True
    stats = {
        "errors": 0,
        "skipped": 0,
        "updated": 0,
        "details": [],
        "error_messages": [],
        "skipped_contacts": [],
    }

    client = MailChimp(settings.MAILCHIMP_KEY)
    contacts_table = Table.objects.filter(table_type=Table.TYPE_CONTACTS).last()

    audience_members_table_fields_defs = table_fields.TABLE_MAPPING['audience_members']
    contact_table_fields_defs = table_fields.TABLE_MAPPING['contact_fields']

    task_result = TaskResult.objects.create(user=user, task=task)

    if not contacts_table:
        success = False
        stats["errors"] += 1
        stats["details"].append(_("Contacts' table does not exist"))
    else:
        all_contacts = utils.get_all_contacts(contacts_table)
        for contact in all_contacts:
            if not "audience_id" in contact.keys():
                print("skipping: ", contact)
                stats["skipped_contacts"].append(str(contact)[:100])
                stats["skipped"] += 1
                continue

            merge_fields = {}
            for mfield in contact_table_fields_defs:
                try:
                    value = contact[mfield]
                except KeyError:
                    continue

                field_def = contact_table_fields_defs[mfield]
                path = field_def.get("mailchimp_path", (mfield, ))
                path_len = len(path)    

                # Build Mailchimp data structure like {'aaa': {'bbb': {'ccc': {'ddd': value}}}} for
                # items which have their path like ('aaa', 'bbb', 'ccc', 'ddd')
                if path_len == 1:
                    merge_fields[path[0]] = value
                elif path_len == 2:
                    merge_fields[path[0]] = merge_fields.get(path[0], {})
                    merge_fields[path[0]][path[1]] = value
                elif path_len == 3:
                    merge_fields[path[0]] = merge_fields.get(path[0], {})
                    merge_fields[path[0]][path[1]] = merge_fields[path[0]].get(path[1], {})
                    merge_fields[path[0]][path[1]][path[2]] = value
                elif path_len == 4:
                    merge_fields[path[0]] = merge_fields.get(path[0], {})
                    merge_fields[path[0]][path[1]] = merge_fields[path[0]].get(path[1], {})
                    merge_fields[path[0]][path[1]][path[2]] = merge_fields[path[0]][path[1]].get(path[2], {})
                    merge_fields[path[0]][path[1]][path[2]][path[3]] = value
                elif path_len == 5:
                    merge_fields[path[0]] = merge_fields.get(path[0], {})
                    merge_fields[path[0]][path[1]] = merge_fields[path[0]].get(path[1], {})
                    merge_fields[path[0]][path[1]][path[2]] = merge_fields[path[0]][path[1]].get(path[2], {})
                    merge_fields[path[0]][path[1]][path[2]][path[3]] = merge_fields[path[0]][path[1]][path[2]].get(path[3], {})
                    merge_fields[path[0]][path[1]][path[2]][path[3]][path[4]] = value
                else:
                    print(_("Mailchimp path too long:"), path)

            # TODO: check which data is read-only so that we don't bother uploading it and maybe automate this dict
            data = {
                "email_address": contact.get("email_address", ""),
                "email_type": contact.get("email_type", "text"),
                "status": contact.get("status", ""),
                "ubsubscribe_reason": contact.get("unsubscribe_reason", ""),
                # "interests": contact.get("interests", ""),
                "language": contact.get("language", ""),
                "vip": bool(contact.get("vip", False)),
                "email_client": contact.get("email_client", ""),
                "source": contact.get("source", ""),
                "status_if_new": "unsubscribed",
                **merge_fields,
            }

            try:
                client.lists.members.create_or_update(
                    contact.get("audience_id"), 
                    contact.get("email_address", ""),  # "subscriber_hash" also accepts the email address
                    data
                )
            except MailChimpError as e:
                print("MAILCHIMP EXCEPTION = ", e)
                stats["errors"] += 1
                try:
                    error_message = '"{}" {}'.format(
                        literal_eval(str(e))["errors"][0]["field"],
                        literal_eval(str(e))["errors"][0]["message"]
                    )
                except (SyntaxError, KeyError):
                    error_message = str(e)
                stats["error_messages"].append(
                    _("First error for {}: {}").format(contact.get("email_address", ""), error_message))
            else:
                stats["updated"] += 1

    stats["details"].append(_("{} contacts created or updated").format(stats["updated"]))
    stats["details"].append(_("{} contacts skipped").format(stats["skipped"]))
    if len(stats["skipped_contacts"]):
        stats["details"].append(", ".join(stats["skipped_contacts"][:5]))
    stats["details"].append(_("{} contacts failed to create or update").format(stats["errors"]))

    if not stats["errors"]:
        task_result.success = success
    else:
        # Only send the first five error messages for display
        for message in stats["error_messages"][:5]:
            stats["details"].append(message)
        if len(stats["error_messages"]) > 5:
            stats["details"].append("...")

    task_result.status = TaskResult.FINISHED
    task_result.stats = stats
    task_result.save()

    return task_result.id, task_result.success


def run_sync(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Exception(_("The sync task with id {} does not exist anymore").format(task_id))

    if request_user_id:
        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if not user:
        user, created = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

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
                stats_details.append(_('<b>{}</b> {} in <b>{}</b>').format(v, k, table))
        task_result.stats['details'] = stats_details
    task_result.date_end = timezone.now()
    task_result.duration = task_result.date_end - task_result.date_start
    task_result.save()
    return task_result.id, task_result.success


def run_segmentation(request_user_id, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Exception(_("The segmentation task with id {} does not exist anymore").format(task_id))

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
        user, created = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

    token, created = Token.objects.get_or_create(user=user)
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
        stats['details'].append(_("Contacts' table does not exist"))
    else:
        if primary_table.table != audience_members_table:
            success = False
            stats['errors'] += 1
            stats['details'].append(
                _('<b>{}</b> needs to be the primary table in <b>{}</b> filtered view').format(
                    audience_members_table, filtered_view.name
                ))
        primary_table_fields =  primary_table.fields.values_list('name', flat=True)
        mandatory_fields = ['audience_id', 'id', 'email_address']
        for field in mandatory_fields:
            if field not in primary_table_fields:
                success = False
                stats['errors'] += 1
                stats['details'].append(
                    _('<b>{}</b> field needs to be selected in the primary table in <b>{}</b> filtered view').format(
                        table_fields.AUDIENCE_MEMBERS_FIELDS[field]['display_name'], filtered_view.name
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
