from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

from api import models as api_models

from celery import shared_task
from plugin_mailchimp import utils, models, serializers

from .table_fields import AUDIENCE_MEMBERS_FIELDS


@shared_task
def hello(a):
    print(a)
    return a


@shared_task
def sync(request, task_id):
    print('start mailchimp sync task')
    task = models.Task.objects.get(pk=task_id)
    if hasattr(request, 'user'):
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username='paul-sync')
    settings = models.Settings.objects.last()

    task_result = models.TaskResult.objects.create(
        user=user,
        task=task)

    KEY = settings.key
    AUDIENCES_TABLE_NAME = settings.audiences_table_name
    AUDIENCES_STATS_TABLE_NAME = settings.audiences_stats_table_name
    AUDIENCE_MEMBERS_TABLE_NAME = settings.audience_members_table_name
    AUDIENCE_SEGMENTS_TABLE_NAME = settings.audience_segments_table_name
    SEGMENT_MEMBERS_TABLE_NAME = settings.segment_members_table_name
    AUDIENCE_TAGS_TABLE_NAME = settings.audience_tags_table_name

    try:
        success, stats = utils.run_sync(
            KEY,
            AUDIENCES_TABLE_NAME,
            AUDIENCES_STATS_TABLE_NAME,
            AUDIENCE_SEGMENTS_TABLE_NAME,
            AUDIENCE_MEMBERS_TABLE_NAME,
            SEGMENT_MEMBERS_TABLE_NAME,
            AUDIENCE_TAGS_TABLE_NAME
        )
        task_result.success = success
        task_result.stats = stats
        task_result.status = 'Finished'
    except Exception as e:
        task_result.success = False
        task_result.status = 'Finished'
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
    print('ended mailchimp sync task')
    return task_result.id, task_result.success


@shared_task
def run_segmentation(request, task_id):
    task = models.Task.objects.get(pk=task_id)
    success = True
    stats = {
        'success': 0,
        'errors': 0,
        'details': []
    }

    if hasattr(request, 'user'):
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username='paul-sync')

    token, _ = Token.objects.get_or_create(user=user)
    settings = models.Settings.objects.last()

    task_result = models.TaskResult.objects.create(
        user=user,
        task=task)

    filtered_view = task.segmentation_task.filtered_view
    primary_table = filtered_view.primary_table

    audience_members_table = api_models.Table.objects.filter(name=settings.audience_members_table_name)

    if not audience_members_table.exists():
        success = False
        stats['errors'] += 1
        stats['details'].append(
            '"{}" does not exists. Run mailchimp import task first.'.format(
                settings.audience_members_table_name
            ))
    else:
        audience_members_table = audience_members_table[0]
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
    task_result.status = 'Finished'
    task_result.save()

    return task_result.id, task_result.success
