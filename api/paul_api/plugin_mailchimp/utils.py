from django.contrib.auth.models import User
from django.utils import timezone
from api import models
from mailchimp3 import MailChimp
from pprint import pprint

from api import views as api_views
from api import models as api_models

from . import table_fields

import requests


def get_or_create_table(table_type, table_name):
    db = models.Database.objects.last()
    user, _ = User.objects.get_or_create(username='paul-sync')

    table, created = models.Table.objects.get_or_create(
        name=table_name,
        database=db,
        owner=user)
    table.last_edit_date = timezone.now()
    table.last_edit_user = user
    table.active = True
    table.save()

    if created:
        table_fields_defs = table_fields.TABLE_MAPPING[table_type]
        for field_name, field_details in table_fields_defs.items():
            column, _ = models.TableColumn.objects.get_or_create(
                table=table,
                name=field_name
                )
            column.display_name = field_details['display_name']
            column.field_type = field_details['type']
            column.save()

    return table


def check_tag_is_present(audience_tags_table_name, audience_id, audience_name, tag):
    user, _ = User.objects.get_or_create(username='paul-sync')
    tags_table, created = models.Table.objects.get_or_create(
        name=audience_tags_table_name,
        database_id=1,
        owner=user,
        active=True)
    if created:
        models.TableColumn.objects.get_or_create(table=tags_table, name='id', display_name='ID', field_type="int")
        models.TableColumn.objects.get_or_create(table=tags_table, name='name', display_name='Name', field_type="enum")
        models.TableColumn.objects.get_or_create(table=tags_table, name='audience_id', display_name='Audience ID', field_type="text")
        models.TableColumn.objects.get_or_create(table=tags_table, name='audience_name', display_name='Audience Name', field_type="text")
    tag_exists = models.Entry.objects.filter(table=tags_table, data__id=tag['id']).exists()
    if not tag_exists:
        tag['audience_id'] = audience_id
        tag['audience_name'] = audience_name
        models.Entry.objects.create(table=tags_table, data=tag)
        return 'created'
    return 'updated'


def run_sync(key,
             audiences_table_name,
             audiences_stats_table_name,
             audience_segments_table_name,
             audience_members_table_name,
             segment_members_table_name,
             audience_tags_table_name):
    '''
    Do the actual sync.

    Return success (bool), updates(json), errors(json)
    '''
    success = True
    stats = {
        audiences_table_name: {
            'created': 0,
            'updated': 0,
        },
        audiences_stats_table_name: {
            'created': 0,
            'updated': 0,
        },
        audience_segments_table_name: {
            'created': 0,
            'updated': 0,
        },
        audience_members_table_name: {
            'created': 0,
            'updated': 0,
        },
        segment_members_table_name: {
            'created': 0,
            'updated': 0,
        },
        audience_tags_table_name: {
            'created': 0,
            'updated': 0,
        }

    }
    try:
        client = MailChimp(key)
        lists = client.lists.all()
    except:
        return False, {'details': [
        "Could not connect to mailchimp. Check <b>KEY</b> "
        " in settings and make sure it has all permissions."]}

    audiences_table = get_or_create_table('audiences', audiences_table_name)
    audiences_stats_table = get_or_create_table('audiences_stats', audiences_stats_table_name)
    audience_segments_table = get_or_create_table('audience_segments', audience_segments_table_name)
    audience_members_table = get_or_create_table('audience_members', audience_members_table_name)
    segment_members_table = get_or_create_table('segment_members', segment_members_table_name)

    audiences_table_fields_defs = table_fields.TABLE_MAPPING['audiences']
    audiences_stats_table_fields_defs = table_fields.TABLE_MAPPING['audiences_stats']
    audience_segments_table_fields_defs = table_fields.TABLE_MAPPING['audience_segments']
    audience_members_table_fields_defs = table_fields.TABLE_MAPPING['audience_members']
    segment_members_table_fields_defs = table_fields.TABLE_MAPPING['segment_members']

    for list in lists['lists']:
        audience_exists = models.Entry.objects.filter(
            table=audiences_table, data__id=list['id'])

        if audience_exists:
            audience_entry = audience_exists[0]
            stats[audiences_table_name]['updated'] += 1
        else:
            stats[audiences_table_name]['created'] += 1
            audience_entry = models.Entry.objects.create(
                table=audiences_table,
                data={'id': list['id']})

        for field in audiences_table_fields_defs:
            field_def = audiences_table_fields_defs[field]
            try:
                if field_def['type'] == 'date':
                    audience_entry.data[field] = list[field][:10]
                else:
                    audience_entry.data[field] = list[field]
            except:
                audience_entry.data[field] = list[field_def['mailchimp_parent_key_name']][field_def['mailchimp_key_name']]

        audience_entry.save()

        # Sync list stats
        audience_stats_exists = models.Entry.objects.filter(
            table=audiences_stats_table, data__audience_id=list['id'])
        if audience_stats_exists:
            audience_stats_entry = audience_stats_exists[0]
            stats[audiences_stats_table_name]['updated'] += 1
        else:
            stats[audiences_stats_table_name]['created'] += 1
            audience_stats_entry = models.Entry.objects.create(
                table=audiences_stats_table,
                data={
                    'audience_id': list['id'],
                    'audience_name': list['name']
                    })
        for field in audiences_stats_table_fields_defs:
            field_def = audiences_stats_table_fields_defs[field]
            try:
                if field_def['type'] == 'date':
                    audience_stats_entry.data[field] = list['stats'][field][:10]
                else:
                    audience_stats_entry.data[field] = list['stats'][field]
            except:
                pass

        audience_stats_entry.save()

        # Sync list segments
        list_segments = client.lists.segments.all(list_id=list['id'], get_all=True)

        for segment in list_segments['segments']:
            # print('     Segment:', segment['name'])
            audience_segments_exists = models.Entry.objects.filter(
                table=audience_segments_table, data__audience_id=segment['list_id'])
            if audience_segments_exists:
                audience_segments_entry = audience_segments_exists[0]
                stats[audience_segments_table_name]['updated'] += 1
            else:
                stats[audience_segments_table_name]['created'] += 1
                audience_segments_entry = models.Entry.objects.create(
                    table=audience_segments_table,
                    data={
                        'audience_id': segment['list_id'],
                        'audience_name': list['name']
                        })
            for field in audience_segments_table_fields_defs:
                field_def = audience_segments_table_fields_defs[field]
                try:
                    if field_def['type'] == 'date':
                        audience_segments_entry.data[field] = segment[field][:10]
                    else:
                        audience_segments_entry.data[field] = segment[field]
                except:
                    pass

            audience_segments_entry.save()

            # Sync segment members
            segment_members = client.lists.segments.members.all(list_id=list['id'], segment_id=segment['id'], get_all=True)

            for member in segment_members['members']:
                # print('         Segment member:', member['email_address'])
                segment_members_exists = models.Entry.objects.filter(
                    table=segment_members_table, data__id=member['id'], data__segment_id=segment['id'])
                if segment_members_exists:
                    segment_members_entry = segment_members_exists[0]
                    stats[segment_members_table_name]['updated'] += 1
                else:
                    stats[segment_members_table_name]['created'] += 1
                    segment_members_entry = models.Entry.objects.create(
                        table=segment_members_table,
                        data={
                            'audience_id': member['list_id'],
                            'segment_id': segment['id'],
                            'audience_name': list['name'],
                            'segment_name': segment['name']
                            })
                for field in segment_members_table_fields_defs:
                    field_def = segment_members_table_fields_defs[field]
                    if field in member.keys():
                        if field_def['type'] == 'enum':
                            # print(segment_members_table, field)
                            table_column = models.TableColumn.objects.get(table=segment_members_table, name=field)
                            if not table_column.choices:
                                table_column.choices = []
                            if 'is_list' in field_def.keys():
                                for item in member[field]:
                                    if item not in table_column.choices:
                                        table_column.choices.append(item)
                                        table_column.save()
                            else:
                                if member[field] not in table_column.choices:
                                    table_column.choices.append(member[field])
                                    table_column.save()
                        if 'is_list' in field_def.keys():
                            segment_members_entry.data[field] = ','.join(member[field])
                        else:
                            if field_def['type'] == 'date':
                                segment_members_entry.data[field] = member[field][:10]
                            else:
                                segment_members_entry.data[field] = member[field]
                    else:
                        try:
                            segment_members_entry.data[field] = member[field_def['mailchimp_parent_key_name']][field_def['mailchimp_key_name']]
                        except Exception as e:
                                pass

                segment_members_entry.save()

        # # Sync list members
        list_members = client.lists.members.all(list_id=list['id'], get_all=True)

        for member in list_members['members']:
            # print('     List member:', member['email_address'])
            member['audience_name'] = list['name']
            audience_members_exists = models.Entry.objects.filter(
                table=audience_members_table, data__id=member['id'], data__audience_id=list['id'])
            if audience_members_exists:
                audience_members_entry = audience_members_exists[0]
                stats[audience_members_table_name]['updated'] += 1
            else:
                stats[audience_members_table_name]['created'] += 1
                audience_members_entry = models.Entry.objects.create(
                    table=audience_members_table,
                    data={
                        'audience_id': member['list_id'],
                        'audience_name': list['name']
                        })

            for field in audience_members_table_fields_defs:
                field_def = audience_members_table_fields_defs[field]
                if field in member.keys():
                    if field_def['type'] == 'enum':
                        table_column = models.TableColumn.objects.get(table=audience_members_table, name=field)
                        if not table_column.choices:
                            # print('no choices', table_column)
                            table_column.choices = []
                        if 'is_list' in field_def.keys():
                            for item in member[field]:
                                if item['name'] not in table_column.choices:
                                    table_column.choices.append(item['name'])
                                    table_column.save()
                        else:
                            if member[field] not in table_column.choices:
                                table_column.choices.append(member[field])
                                # print('append', member[field])
                                table_column.save()
                    if 'is_list' in field_def.keys():
                        items = []
                        for item in member[field]:
                            tag_status = check_tag_is_present(audience_tags_table_name, list['id'], list['name'], item)
                            items.append(item['name'])
                            stats[audience_tags_table_name][tag_status] += 1
                        audience_members_entry.data[field] = ','.join(items)
                    else:
                        if field_def['type'] == 'enum':
                            audience_members_entry.data[field] = member[field][:10]
                        else:
                            audience_members_entry.data[field] = member[field]
                else:
                    try:
                        audience_members_entry.data[field] = member[field_def['mailchimp_parent_key_name']][field_def['mailchimp_key_name']]
                    except Exception as e:
                        pass

            audience_members_entry.save()
    return success, stats


def add_list_to_segment(settings,
             lists_users,
             tag):
    '''
    Do the actual sync.

    Return success (bool), updates(json), errors(json)
    '''
    success = True
    stats = {
        'success': 0,
        'errors': 0,
        'details': []
    }

    client = MailChimp(settings.key)
    data = {
        'tags': [{'name': tag, 'status': 'active'}]
    }

    for audience, subcribers in lists_users.items():
        for subscriber_hash in subcribers:
            try:
                x = client.lists.members.tags.update(list_id=audience, subscriber_hash=subscriber_hash, data=data)
                stats['success'] += 1
            except:
                success = False
                stats['errors'] += 1
                stats['details'].append('{} could not be updated (mailchimp error)'.format(email))

    if stats['success']:
        stats['details'].append('<b>{}</b> members were updated with tag <b>{}</b>'.format(stats['success'], tag))
    if stats['errors']:
        stats['details'].append('<b>{}</b> members were not updated with tag <b>{}</b>'.format(stats['errors'], tag))
    return success, stats


def get_emails_from_filtered_view(token, filtered_view, settings):
    page = 1
    continue_request = True
    results = []
    headers = {'Authorization': 'Token ' + token.key}

    while continue_request:
        url = 'http://api:8000/api/filters/{}/entries/?page={}'.format(filtered_view.pk, page)
        r = requests.get(url, headers=headers).json()
        results += r['results']
        if r['links']['next']:
            page += 1
        else:
            continue_request = False

    audience_members_table = api_models.Table.objects.get(
        name=settings.audience_members_table_name)

    lists = {}
    user_hash_field = '{}__{}'.format(audience_members_table.slug, 'id')
    audience_id_field = '{}__{}'.format(
        audience_members_table.slug, 'audience_id')
    for entry in results:
        if entry[user_hash_field] not in lists.get(entry[audience_id_field], []):
            lists.setdefault(entry[audience_id_field], [])
            lists[entry[audience_id_field]].append(entry[user_hash_field])
    return lists
