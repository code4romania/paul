from django.db.models import (
    Count, Sum, Min, Max, Avg,
    DateTimeField, CharField, FloatField, IntegerField, Q)
from django.db.models.functions import Trunc, Cast
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.urls import reverse
from django.utils import timezone

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from collections import OrderedDict
import inflection

# from api.views import FilterViewSet
from . import models

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import re
from pprint import pprint

DB_FUNCTIONS = {
    "Count": Count,
    "Sum": Sum,
    "Min": Min,
    "Max": Max,
    "Avg": Avg,
}


def send_email(template, context, subject, to):
    html = get_template(template)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(
        subject, html_content, settings.NO_REPLY_EMAIL, [to])
    msg.attach_alternative(html_content, "text/html")

    return msg.send()


def snake_case(text):
    value = inflection.underscore(inflection.parameterize(text))
    return re.sub('_+', '_', value)


def import_csv(reader, table, csv_import=None):
    errors_count = 0
    import_count_created = 0
    import_count_updated = 0
    errors = []
    if csv_import:
        csv_field_mapping = {x.original_name: x for x in csv_import.csv_field_mapping.exclude(table_column=None)}
    else:
        csv_field_mapping = {x.original_name: x for x in table.csv_field_mapping.all()}
    table_fields = {x.name: x for x in table.fields.all()}
    field_choices = {x.name: x.choices for x in table.fields.all()}
    i = 0
    unique_fields = {field_map.table_column.name:field_map.original_name for field, field_map in csv_field_mapping.items() if field_map.unique==True}
    for row in reader:
        i += 1
        entry_dict = {}
        error_in_row = False
        errors_in_row = {}
        
        try:
            for key, field in csv_field_mapping.items():
                if csv_import:
                    if field.table_column:
                        field_name = field.table_column.name
                        field_type = field.table_column.field_type
                else:
                    field_name = snake_case(field.display_name)
                    field_type = field.field_type
                try:
                    if row[key]:
                        if field_type == "int":
                            entry_dict[field_name] = int(row[key])
                        elif field_type == "float":
                            entry_dict[field_name] = float(row[key])
                        elif field_type == "date":
                            value = datetime.strptime(row[key], field.field_format)
                            entry_dict[field_name] = value.strftime('%Y-%m-%d')
                        elif field_type == "enum":
                            value = row[key]
                            if not field_choices[field_name]:
                                field_choices[field_name] = []
                            if value not in field_choices[field_name]:
                                field_choices[field_name].append(value)
                                table_fields[field_name].choices = list(set(field_choices[field_name]))
                                table_fields[field_name].save()
                            entry_dict[field_name] = value
                        else:
                            entry_dict[field_name] = row[key]
                    else:
                        print(table_fields)
                        print(csv_field_mapping)
                        if table_fields[field_name].required or csv_field_mapping[key].required:
                            error_in_row = True
                            errors_in_row[key] = "Acest câmp este obligatoriu"
                        entry_dict[field_name] = None
                except Exception as e:
                    # print(e)
                    error_in_row = True
                    errors_in_row[key] = e.__class__.__name__
                    # errors_in_row[key] = str(e)
            if not error_in_row:
                entry = None
                if unique_fields:
                    # print('check unique')
                    data = {}
                    for field in unique_fields:
                        data[field] = entry_dict[field]
                    # print(data)
                    try:
                        entry, created = models.Entry.objects.get_or_create(table=table, data__contains=data)
                        if created:
                            import_count_created += 1
                        else:
                            import_count_updated += 1
                    except:
                        error_in_row = True
                        for field in unique_fields:
                            errors_in_row[unique_fields[field]] = 'Acest camp trebuie sa fie unic în tabel'
                        errors.append({"row": row, "errors": errors_in_row})
                        errors_count += 1
                else:
                    entry = models.Entry.objects.create(table=table)
                    import_count_created += 1

                if entry:
                    entry.data = entry_dict
                    entry.save()
            else:
                errors.append({"row": row, "errors": errors_in_row})
                errors_count += 1

        except Exception as e:
            # print(e)
            errors_count += 1

    # print("errors: {} import_count_created: {} import_count_updated: {}".format(errors_count, import_count_created, import_count_updated))
    return errors, errors_count, import_count_created, import_count_updated


def get_chart_data(request, chart, table, preview=False):
    y_axis_function = DB_FUNCTIONS[chart.y_axis_function]

    table_fields = {x.name: x.field_type for x in table.fields.all()}
    filter_dict = request_get_to_filter(request.GET, table_fields, Q(), False)

    chart_data = models.Entry.objects \
        .filter(table=chart.table) \
        .filter(filter_dict)
    if preview:
        chart_data = chart_data[:100]

    if chart.timeline_field:

        chart_data = chart_data.annotate(date_field=Cast(
                KeyTextTransform(chart.timeline_field.name, "data"), DateTimeField()
            )) \
            .annotate(time=Trunc('date_field', chart.timeline_period.lower(), is_dst=False)) \
            .values('time')
    else:
        chart_data = chart_data \
            .annotate(series=Cast(
                KeyTextTransform(chart.x_axis_field.name, "data"), CharField()))
        if chart.x_axis_field_2:
            chart_data = chart_data \
                .annotate(series_group=Cast(
                    KeyTextTransform(chart.x_axis_field_2.name, "data"), CharField()))\
                .values('series', 'series_group')
        else:
            chart_data = chart_data.values('series')

    # if we have Y axis field
    if chart.y_axis_field:
        chart_data = chart_data \
            .annotate(value=y_axis_function(Cast(
                KeyTextTransform(chart.y_axis_field.name, "data"), FloatField()
            )))
    else:
        chart_data = chart_data.annotate(value=Count('id'))

    # if we have X axis field
    if chart.x_axis_field and chart.timeline_field:
        chart_data = chart_data \
            .annotate(series=Cast(
                KeyTextTransform(chart.x_axis_field.name, "data"), CharField()
            ))
        if chart.x_axis_field_2:
            chart_data = chart_data \
                .annotate(series_group=Cast(
                    KeyTextTransform(chart.x_axis_field_2.name, "data"), CharField()))\
                .values('time', 'series', 'series_group', 'value')
        else:
            chart_data = chart_data.values('time', 'value', 'series')
    elif chart.x_axis_field:
        if chart.x_axis_field_2:
            chart_data = chart_data.values('series', 'series_group', 'value')
        else:
            chart_data = chart_data.values('series', 'value')

    if chart.timeline_field:
        chart_data = chart_data.order_by('time')
        data = prepare_chart_data(chart, chart_data, timeline=True)
    else:
        chart_data = chart_data.order_by('data__' +  chart.x_axis_field.name)
        data = prepare_chart_data(chart, chart_data, timeline=False)

    return data


def get_strftime(date, period):
    if not date:
        return None
    if period == 'year':
        date_str = date.strftime('%Y')
    elif period == 'month':
        date_str = date.strftime('%Y-%m')
    elif period == 'week':
        date_str = date.strftime('%Y-%V')
    elif period == 'day':
        date_str = date.strftime('%Y-%m-%d')
    elif period == 'hour':
        date_str = date.strftime('%Y-%m-%d %H')
    elif period == 'minute':
        date_str = date.strftime('%Y-%m-%d %H:%M')
    return date_str


def get_strptime(date_str, period):
    if period == 'year':
        date = datetime.strptime(date_str, '%Y')
    elif period == 'month':
        date = datetime.strptime(date_str, '%Y-%m')
    elif period == 'week':
        date = datetime.strptime(date_str + '-1', '%G-%V-%w')
    elif period == 'day':
        date = datetime.strptime(date_str, '%Y-%m-%d')
    elif period == 'hour':
        date = datetime.strptime(date_str, '%Y-%m-%d %H')
    elif period == 'minute':
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    return date


def prepare_chart_data(chart, chart_data, timeline=True):
    data_dict = {}
    timeline_period = chart.timeline_period
    data = {
        'labels': [],
        'datasets': [{
            'label': '',
            'data': []
        }],
        # 'options': {}
    }
    colors = ['#223E6D','#87C700','#8E0101','#FF6231','#175B1E','#A2D3E4','#4B0974','#ED1A3B','#0081BB','#9CCB98','#DF3D84','#FD7900','#589674','#C2845D','#AA44E8','#EFAD88','#8590FF','#00B3A8','#FF8DB8','#FBB138']
    colors.reverse()
    if timeline == False:
        has_series_group = False
        for entry in chart_data:
            if 'series_group' in entry.keys():
                has_series_group = True
                data_dict.setdefault(entry['series'], {})
                data_dict[entry['series']].setdefault(entry['series_group'], 0)
                data_dict[entry['series']][entry['series_group']] = entry['value']
            else:
                data_dict.setdefault(entry['series'], 0)
                data_dict[entry['series']] = entry['value']
        if not has_series_group:
            i = 0
            data['datasets'][0]['backgroundColor'] = []
            for key, value in data_dict.items():
                i += 1
                data['labels'].append(key)
                if chart.x_axis_field:
                    data['datasets'][0]['label'] = chart.x_axis_field.display_name
                data['datasets'][0]['data'].append(value)
                if chart.chart_type in ['Pie', 'Doughnut']:
                    data['datasets'][0]['backgroundColor'].append(colors[i%20])
                elif chart.chart_type in ['Line']:
                    data['datasets'][0]['backgroundColor'] = 'rgba(0, 0, 0, 0)'
                    data['datasets'][0]['borderColor'] = colors[0]
                else:
                    data['datasets'][0]['backgroundColor'] = colors[0]
        else:
            data['datasets'] = []
            labels = []
            labels_dict = {}
            for serie, group in data_dict.items():
                data['labels'].append(serie)
                for group_name in group:
                    if group_name not in labels:
                        labels.append(group_name)
            for serie, group in data_dict.items():
                for label in labels:
                    labels_dict.setdefault(label, [])
                    labels_dict[label].append(group.get(label, 0))

            i = 0
            for label, label_values in labels_dict.items():
                i += 1
                if chart.chart_type == 'Line':
                    dataset = {
                        'label': label,
                        'data': label_values,
                        'backgroundColor': 'rgba(0, 0, 0, 0)',
                        'borderColor': colors[i % 10]
                    }
                else:
                    dataset = {
                        'label': label,
                        'data': label_values,
                        'backgroundColor': colors[i % 10]
                    }
                data['datasets'].append(dataset)
    else:
        labels = []
        labels_dict = {}

        for entry in chart_data:
            time = get_strftime(entry['time'], timeline_period)
            data_dict.setdefault(time, {})
            data_dict[time][entry.get('series', '')] = entry['value']
            if entry.get('series', '') not in labels:
                labels.append(entry.get('series', ''))

        if chart.timeline_include_nulls:
            first_entry = list(data_dict)[0]
            last_entry = get_strptime(list(data_dict)[-1], timeline_period)
            relativetime_increment = {}
            relativetime_increment[timeline_period + 's'] = 1

            time_period = get_strptime(first_entry, timeline_period)

            ordered_data_dict = OrderedDict()
            while time_period <= last_entry:
                time_period_str = get_strftime(time_period, timeline_period)
                data_dict.setdefault(time_period_str, {})
                ordered_data_dict[time_period_str] = data_dict[time_period_str]
                time_period += relativedelta(**relativetime_increment)
            data_dict = ordered_data_dict

        for key, value in data_dict.items():
            data['labels'].append(key)

            for label in labels:
                labels_dict.setdefault(label, [])
                labels_dict[label].append(value.get(label, 0))

        data['datasets'] = []
        i = 0
        for label, label_values in labels_dict.items():
            i += 1
            if chart.chart_type == 'Line':
                dataset = {
                    'label': label,
                    'data': label_values,
                    'backgroundColor': 'rgba(0, 0, 0, 0)',
                    'borderColor': colors[i % 10]
                }
            else:
                dataset = {
                    'label': label,
                    'data': label_values,
                    'backgroundColor': colors[i % 10]
                }
            data['datasets'].append(dataset)

    if chart.y_axis_field:
        y_axis_label = '{} ({})'.format(chart.y_axis_function, chart.y_axis_field.display_name)
    else:
        y_axis_label = chart.y_axis_function
    if chart.x_axis_field:
        if chart.timeline_field:
            x_axis_label = '{} ({})'.format(chart.x_axis_field.display_name, chart.timeline_field.display_name)
        else:
            x_axis_label = chart.x_axis_field.display_name
    else:
        if chart.timeline_field:
            x_axis_label = '{} ({})'.format(chart.timeline_field.display_name, timeline_period.capitalize())
        else:
            x_axis_label = chart.table.name

    data['options'] = {
        'maintainAspectRatio': False,
        'tooltips': {
            'mode': 'index',
            'position': 'nearest'
        },
        'scales': {
            'yAxes': [{
                'scaleLabel': {
                    'display': True,
                    'labelString': y_axis_label
                }
            }],
            'xAxes': [{
                'scaleLabel': {
                    'display': True,
                    'labelString': x_axis_label
                }
            }]
        } if chart.chart_type not in ['Pie', 'Doughnut'] else {}
      }

    return data


def request_get_to_filter(request, table_fields, filter_dict=Q(), is_filter=False):
    # print(request)
    for key in request:
        if is_filter:
            table = key.split("__")[0]
            filter_table_field = "__".join(key.split("__")[:2])
            key = "__".join(key.split("__")[1:])

            filter_dict.setdefault(table, {})
            filter_dict_table = filter_dict[table]
        else:
            filter_dict_table = filter_dict
            filter_table_field = ''
        column = key.split("__")[0]

        if key and (column in table_fields.keys() or filter_table_field in table_fields.keys()):
            if is_filter:
                column_type = table_fields[filter_table_field]
                value = request.get(table + '__' + key).split(",")
            else:
                column_type = table_fields[column]
                value = request.get(key).split(",")
            key_lookup = key.split("__")[-1]

            if len(value) == 1:
                value = value[0]
            else:
                key = key + "__in"

            if value == '__BLANK':
                filter_dict_table = filter_dict_table & Q(
                    Q(
                        **{"data__{}__isnull".format(key): True}) | Q(
                        **{"data__{}".format(key): ''})
                    )
            else:
                if column_type in [
                    "float",
                    "int",
                ]:
                    filter_dict_table = filter_dict_table & Q(
                        **{"data__{}".format(key): float(value)})
                else:
                    if column_type == 'date':
                        if key_lookup == 'relative':
                            relative_type = value.split('_')[0] # current | next | last
                            relative_period = value.split('_')[-1] + 's' # day | week | month | year
                            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                            relative_increment_dict = {}

                            if relative_type in ['current', 'next']:
                                relative_increment = 0 if relative_type == 'current' else 1
                                relative_increment_dict[relative_period] = relative_increment
                                date_start = today + relativedelta(**relative_increment_dict)
                                pprint(relative_increment_dict)
                            else:
                                relative_increment_dict[relative_period] = 1
                                date_start = today - relativedelta(**relative_increment_dict)

                            if relative_period == 'weeks':
                                date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0)
                                date_start = date_start - relativedelta(
                                    days=(date_start.isoweekday()-1) % 7, hours=2)
                            elif relative_period == 'months':
                                date_start = date_start.replace(day=1) - relativedelta(hours=2)
                            elif relative_period == 'years':
                                date_start = date_start.replace(month=1, day=1) - relativedelta(hours=2)
                            elif relative_period == 'days':
                                date_start = date_start - relativedelta(hours=2)


                            filter_dict_table = filter_dict_table & Q(
                                **{"data__{}__gte".format(column): date_start})
                            filter_dict_table = filter_dict_table & Q(
                                **{"data__{}__lt".format(column): date_start + relativedelta(**{relative_period:1})})
                        else:
                            # filter_dict_table["data__{}".format(key)] = value
                            filter_dict_table = filter_dict_table & Q(
                                **{"data__{}".format(key): value})
                            # filter_dict_table = {'data__data_nasterii__gte': '1987-06-25'}
                            # print(key, value[:10])
                            # print('===')

                    else:
                        filter_dict_table = filter_dict_table & Q(
                                **{"data__{}".format(key): value})
                        # filter_dict_table["data__{}".format(key)] = value
        if is_filter:
            filter_dict[table] = filter_dict_table
        else:
            filter_dict = filter_dict_table
    pprint(filter_dict)
    return filter_dict


def get_card_data(request, card, table, preview=False):
    data_column_function = DB_FUNCTIONS[card.data_column_function]

    table_fields = {x.name: x.field_type for x in table.fields.all()}
    filter_dict = request_get_to_filter(request.GET, table_fields, Q(), False)

    card_data = models.Entry.objects \
        .filter(table=card.table) \
        .filter(filter_dict)

    if preview:
        card_data = card_data[:100]
    if card.data_column:
        data = card_data \
            .aggregate(value=data_column_function(Cast(
                KeyTextTransform(card.data_column.name, "data"), FloatField()
            )))

    else:
        data = card_data \
            .aggregate(value=data_column_function('id'))

    if data['value'] is None:
        data['value'] = 0

    return data


def pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd %dh %dm %ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh %dm %ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm %ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)