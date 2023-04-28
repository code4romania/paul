import functools
import operator
import requests

from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

from api.models import (
    Table,
    Database,
    TableColumn,
    Entry
)
from api.serializers.entries import EntryDataSerializer
from plugin_mailchimp.models import Settings as MailchimpSettings
from plugin_mailchimp import table_fields


def get_field_value(field_name: str, field_def: dict, source: dict) -> str:
    # Raises KeyError
    if ("mailchimp_path" in field_def) and len(field_def["mailchimp_path"]):
        # if mailchimp_path = ('aaa', 'bbb', 'field_name') then
        # try to get the value of source['aaa']['bbb']['field_name']
        path = field_def["mailchimp_path"]
        value = source.get(path[0])
        for p in path[1:]:
            if type(value) is not dict:
                # We cannot continue down the chain because
                # the previous level value was not a dict
                raise KeyError
            value = value[p]
    else:
        # just get source['field_name']
        path = field_name
        value = source[path]
    return value


def is_list_field(field_def: dict) -> bool:
    if "is_list" in field_def.keys():
        return bool(field_def["is_list"])
    else:
        return False


def create_mailchimp_tables(audiences_name: str="") -> int:
    mc_settings = MailchimpSettings.objects.latest()

    get_or_create_table(mc_settings.audiences_table_name, 'audiences')
    get_or_create_table(mc_settings.audiences_stats_table_name, 'audiences_stats')
    get_or_create_table(mc_settings.audience_segments_table_name, 'audience_segments')
    
    # TODO: This table should be created by the user, not automatically
    contact_table = get_or_create_table(
        audiences_name, 'contact_fields', 'audience_members')
    contact_table.table_type = Table.TYPE_CONTACTS
    contact_table.save()
    
    get_or_create_table(mc_settings.segment_members_table_name, 'segment_members')

    return contact_table.id


def get_or_create_table(table_name: str, *table_rulesets: str) -> Table:
    
    if not len(table_rulesets):
        raise ValueError(_("No table rulesets provided"))

    db = Database.objects.last()
    user, created = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)

    table, created = Table.objects.get_or_create(
        name=table_name,
        database=db,
        owner=user)
    table.last_edit_date = timezone.now()
    table.last_edit_user = user
    table.active = True
    table.save()

    if created:
        # Combine all required table definitions into a single one
        mappings = [table_fields.TABLE_MAPPING[ruleset] for ruleset in table_rulesets]
        table_fields_defs = functools.reduce(operator.ior, mappings, {})
        
        for field_name, field_details in table_fields_defs.items():
            column, created = TableColumn.objects.get_or_create(
                table=table,
                name=field_name
            )
            column.display_name = field_details['display_name']
            column.field_type = field_details['type']
            column.save()

    return table


def check_tag_is_present(audience_tags_table_name: str, audience_id: str, audience_name: str, tag) -> str:
    user, created = User.objects.get_or_create(username=settings.TASK_DEFAULT_USERNAME)
    db = Database.objects.last()
    tags_table, created = Table.objects.get_or_create(  # TODO: Fixme!
        name=audience_tags_table_name,
        database_id=db,
        owner=user,
        active=True)
    if created:
        TableColumn.objects.get_or_create(table=tags_table, name='id', display_name='ID', field_type="int")
        TableColumn.objects.get_or_create(table=tags_table, name='name', display_name='Name', field_type="enum")
        TableColumn.objects.get_or_create(table=tags_table, name='audience_id', display_name='Audience ID', field_type="text")
        TableColumn.objects.get_or_create(table=tags_table, name='audience_name', display_name='Audience Name', field_type="text")
    tag_exists = Entry.objects.filter(table=tags_table, data__id=tag['id']).exists()
    if not tag_exists:
        tag['audience_id'] = audience_id
        tag['audience_name'] = audience_name
        Entry.objects.create(table=tags_table, data=tag)
        return 'created'
    return 'updated'


def retrieve_lists_data(client: MailChimp):
    '''
    Do the actual sync.

    Return success (bool), updates(json), errors(json)
    '''
    success = True

    audience_members_table = Table.objects.filter(table_type=Table.TYPE_CONTACTS).last()
    audience_members_table_name = audience_members_table.name

    mc_settings = MailchimpSettings.objects.latest()
    audiences_table_name = mc_settings.audiences_table_name
    audiences_stats_table_name = mc_settings.audiences_stats_table_name
    audience_segments_table_name = mc_settings.audience_segments_table_name
    segment_members_table_name = mc_settings.segment_members_table_name
    audience_tags_table_name = mc_settings.audience_tags_table_name

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
        lists = client.lists.all()
    except:
        return (
            False, {
                "details": [_("Could not connect to mailchimp. Check API Key.")]
            }
        )

    audiences_table = Table.objects.get(name=audiences_table_name)
    audiences_stats_table = Table.objects.get(name=audiences_stats_table_name)
    audience_segments_table = Table.objects.get(name=audience_segments_table_name)
    segment_members_table = Table.objects.get(name=segment_members_table_name)

    audiences_table_fields_defs = table_fields.TABLE_MAPPING['audiences']
    audiences_stats_table_fields_defs = table_fields.TABLE_MAPPING['audiences_stats']
    audience_segments_table_fields_defs = table_fields.TABLE_MAPPING['audience_segments']
    audience_members_table_fields_defs = table_fields.TABLE_MAPPING['audience_members']
    contact_table_fields_defs = table_fields.TABLE_MAPPING['contact_fields']
    segment_members_table_fields_defs = table_fields.TABLE_MAPPING['segment_members']

    for mlist in lists['lists']:
        audience_exists = Entry.objects.filter(
            table=audiences_table, data__id=mlist['id'])

        if audience_exists:
            audience_entry = audience_exists[0]
            stats[audiences_table_name]['updated'] += 1
        else:
            stats[audiences_table_name]['created'] += 1
            audience_entry = Entry.objects.create(
                table=audiences_table,
                data={'id': mlist['id']})

        for field in audiences_table_fields_defs:
            field_def = audiences_table_fields_defs[field]
            field_value = get_field_value(field, field_def, mlist)
            if field_def['type'] == 'date':
                audience_entry.data[field] = field_value[:10]
            else:
                audience_entry.data[field] = field_value

        audience_entry.save()

        # Sync list stats
        audience_stats_exists = Entry.objects.filter(
            table=audiences_stats_table, data__audience_id=mlist['id'])
        if audience_stats_exists:
            audience_stats_entry = audience_stats_exists[0]
            stats[audiences_stats_table_name]['updated'] += 1
        else:
            stats[audiences_stats_table_name]['created'] += 1
            audience_stats_entry = Entry.objects.create(
                table=audiences_stats_table,
                data={
                    'audience_id': mlist['id'],
                    'audience_name': mlist['name']
                    })
        
        for field in audiences_stats_table_fields_defs:
            field_def = audiences_stats_table_fields_defs[field]

            try:
                field_value = get_field_value(field, field_def, mlist)
            except KeyError:
                continue
            
            if field_def['type'] == 'date':
                audience_stats_entry.data[field] = field_value[:10]
            else:
                audience_stats_entry.data[field] = field_value

        audience_stats_entry.save()

        # Sync list segments
        list_segments = client.lists.segments.all(list_id=mlist['id'], get_all=True)

        for segment in list_segments['segments']:
            audience_segments_exists = Entry.objects.filter(
                table=audience_segments_table, data__audience_id=segment['list_id'])
            if audience_segments_exists:
                audience_segments_entry = audience_segments_exists[0]
                stats[audience_segments_table_name]['updated'] += 1
            else:
                stats[audience_segments_table_name]['created'] += 1
                audience_segments_entry = Entry.objects.create(
                    table=audience_segments_table,
                    data={
                        'audience_id': segment['list_id'],
                        'audience_name': mlist['name']
                        })
            for field in audience_segments_table_fields_defs:
                field_def = audience_segments_table_fields_defs[field]

                try:
                    field_value = get_field_value(field, field_def, segment)
                except KeyError:
                    continue

                if field_def['type'] == 'date':
                    audience_segments_entry.data[field] = field_value[:10]
                else:
                    audience_segments_entry.data[field] = field_value

            audience_segments_entry.save()

            # Sync segment members
            segment_members = client.lists.segments.members.all(list_id=mlist['id'], segment_id=segment['id'], get_all=True)

            for member in segment_members['members']:
                segment_members_exists = Entry.objects.filter(
                    table=segment_members_table, data__id=member['id'], data__segment_id=segment['id'])
                if segment_members_exists:
                    segment_members_entry = segment_members_exists[0]
                    stats[segment_members_table_name]['updated'] += 1
                else:
                    stats[segment_members_table_name]['created'] += 1
                    segment_members_entry = Entry.objects.create(
                        table=segment_members_table,
                        data={
                            'audience_id': member['list_id'],
                            'segment_id': segment['id'],
                            'audience_name': mlist['name'],
                            'segment_name': segment['name']
                            })
                for field in segment_members_table_fields_defs:
                    field_def = segment_members_table_fields_defs[field]
                    
                    try:
                        field_value = get_field_value(field, field_def, member)
                    except KeyError:
                        continue

                    if field_def['type'] == 'enum':
                        table_column = TableColumn.objects.get(table=segment_members_table, name=field)
                        
                        if not table_column.choices:
                            table_column.choices = []
                        if is_list_field(field_def):
                            for item in field_value:
                                if item not in table_column.choices:
                                    table_column.choices.append(item)
                                    table_column.save()
                        else:
                            if field_value not in table_column.choices:
                                table_column.choices.append(field_value)
                                table_column.save()
                    if is_list_field(field_def):
                        segment_members_entry.data[field] = ','.join(field_value)
                    else:
                        if field_def['type'] == 'date':
                            segment_members_entry.data[field] = field_value[:10]
                        else:
                            segment_members_entry.data[field] = field_value

                segment_members_entry.save()

        # # Sync list members
        list_members = client.lists.members.all(list_id=mlist['id'], get_all=True)

        for member in list_members['members']:
            member['audience_name'] = mlist['name']
            audience_members_exists = Entry.objects.filter(
                table=audience_members_table, data__id=member['id'], data__audience_id=mlist['id'])
            if audience_members_exists:
                audience_members_entry = audience_members_exists[0]
                stats[audience_members_table_name]['updated'] += 1
            else:
                stats[audience_members_table_name]['created'] += 1
                audience_members_entry = Entry.objects.create(
                    table=audience_members_table,
                    data={
                        'audience_id': member['list_id'],
                        'audience_name': mlist['name']
                        })

            audience_and_contact_fields_defs = audience_members_table_fields_defs | contact_table_fields_defs
            for field in audience_and_contact_fields_defs:
                field_def = audience_and_contact_fields_defs[field]

                try:
                    field_value = get_field_value(field, field_def, member)
                except KeyError:
                    continue
                except Exception as e:
                    print(e)
                    raise e
                
                if field_def['type'] == 'enum':
                    table_column = TableColumn.objects.get(table=audience_members_table, name=field)
                    if not table_column.choices:
                        table_column.choices = []
                    if is_list_field(field_def):
                        for item in field_value:
                            if item['name'] not in table_column.choices:
                                table_column.choices.append(item['name'])
                                table_column.save()
                    else:
                        if field_value not in table_column.choices:
                            table_column.choices.append(field_value)
                            table_column.save()

                if is_list_field(field_def):
                    items = []
                    for item in field_value:
                        tag_status = check_tag_is_present(audience_tags_table_name, mlist['id'], mlist['name'], item)
                        items.append(item['name'])
                        stats[audience_tags_table_name][tag_status] += 1
                    audience_members_entry.data[field] = ','.join(items)
                else:
                    if field_def['type'] == 'enum':  # TODO: ???
                        audience_members_entry.data[field] = field_value[:10]
                    else:
                        audience_members_entry.data[field] = field_value

            audience_members_entry.save()
    return success, stats


def add_list_to_segment(client: MailChimp, lists_users, tag: str):
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

    data = {
        'tags': [{'name': tag, 'status': 'active'}]
    }

    for audience, subcribers in lists_users.items():
        for subscriber_hash in subcribers:
            try:
                x = client.lists.members.tags.update(list_id=audience, subscriber_hash=subscriber_hash, data=data)
                stats['success'] += 1
            except MailChimpError as e:
                print(e)
                success = False
                stats['errors'] += 1
                stats['details'].append(_('{} could not be updated (Mailchimp error)').format(subscriber_hash))

    if stats['success']:
        stats['details'].append(_('<b>{}</b> members were updated with tag <b>{}</b>').format(stats['success'], tag))
    if stats['errors']:
        stats['details'].append(_('<b>{}</b> members were not updated with tag <b>{}</b>').format(stats['errors'], tag))
    return success, stats


def get_emails_from_filtered_view(token, filtered_view):
    page = 1
    continue_request = True
    results = []
    headers = {'Authorization': 'Token ' + token.key}

    while continue_request:  # TODO: get rid of web request
        url = 'http://{}/api/filters/{}/entries/?page={}'.format(
            settings.ALLOWED_HOSTS[0],
            filtered_view.pk, 
            page
        )
        r = requests.get(url, headers=headers).json()
        results += r['results']
        if r['links']['next']:
            page += 1
        else:
            continue_request = False

    lists = {}
    audience_members_table = Table.objects.filter(table_type=Table.TYPE_CONTACTS).last()
    user_hash_field = '{}__{}'.format(audience_members_table.slug, 'id')
    audience_id_field = '{}__{}'.format(
        audience_members_table.slug, 'audience_id')

    for entry in results:
        if entry[user_hash_field] not in lists.get(entry[audience_id_field], []):
            lists.setdefault(entry[audience_id_field], [])
            lists[entry[audience_id_field]].append(entry[user_hash_field])

    return lists


def get_all_contacts(contacts_table):
    table_fields = {x.name: x.field_type for x in contacts_table.fields.all().order_by("id")}
    fields = [x for x in table_fields.keys()]
    context = {
        "table": contacts_table,
        "fields": fields,
    }

    contacts = []
    for entry in contacts_table.entries.order_by("id"):
        contacts.append(EntryDataSerializer(entry, context=context).data)

    return contacts
