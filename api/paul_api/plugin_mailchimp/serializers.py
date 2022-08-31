from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers


from api import utils as api_utils
from api.serializers.users import OwnerSerializer
from api.serializers import (
    WritableSerializerMethodField,
    TaskScheduleCrontabSerializer,
    TaskScheduleSerializer
    )

from plugin_mailchimp import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask

import json
from pprint import pprint


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Settings
        fields = [
            "key",
            "audiences_table_name",
            "audiences_stats_table_name",
            "audience_segments_table_name",
            "audience_members_table_name",
            "segment_members_table_name",
            "audience_tags_table_name",
        ]


class TaskListSerializer(serializers.ModelSerializer):
    last_edit_user = OwnerSerializer(read_only=True)
    schedule_enabled = serializers.SerializerMethodField()

    crontab = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="plugin_mailchimp:task-detail")

    class Meta:
        model = models.Task
        fields = [
            "url",
            "id",
            "name",
            "schedule_enabled",
            "task_type",
            "crontab",
            "last_edit_date",
            "last_run_date",
            "last_edit_user",
        ]


    def get_crontab(self, obj):
        if obj.periodic_task:
            return '{} {} {} {} {}'.format(
                obj.periodic_task.crontab.minute,
                obj.periodic_task.crontab.hour,
                obj.periodic_task.crontab.day_of_week,
                obj.periodic_task.crontab.day_of_month,
                obj.periodic_task.crontab.month_of_year)

        return None

    def get_schedule_enabled(self, obj):
        if obj.periodic_task:
            return obj.periodic_task.enabled
        return False


class SegmentationTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SegmentationTask
        fields = [
            "filtered_view",
            # "email_field",
            # "audience_id",
            "tag",
        ]



class TaskSerializer(serializers.ModelSerializer):
    last_edit_user = OwnerSerializer(read_only=True)
    segmentation_task = SegmentationTaskSerializer(required=False)
    task_results = serializers.SerializerMethodField()
    periodic_task = TaskScheduleSerializer()
    schedule_enabled = serializers.SerializerMethodField()

    class Meta:
        model = models.Task
        fields = [
            "id",
            "name",
            "task_results",
            "task_type",
            "segmentation_task",
            "periodic_task",
            "schedule_enabled",
            "last_edit_date",
            "last_edit_user",
        ]

    def get_task_results(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse(
                "plugin_mailchimp:task-results-list",
                kwargs={"task_pk": obj.pk}))

    def get_schedule_enabled(self, obj):
        if obj.periodic_task:
            return obj.periodic_task.enabled
        return False


class TaskCreateSerializer(serializers.ModelSerializer):
    last_edit_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    last_edit_date = serializers.HiddenField(default=timezone.now())
    segmentation_task = SegmentationTaskSerializer(
        required=False, allow_null=True)
    periodic_task = TaskScheduleSerializer(required=False)

    class Meta:
        model = models.Task
        fields = [
            "id",
            "name",
            "task_type",
            "segmentation_task",
            "last_edit_date",
            "last_edit_user",
            "periodic_task"
        ]

    def create(self, validated_data):
        task_type = validated_data['task_type']
        segment_data = validated_data.pop('segmentation_task')
        periodic_task = None

        if validated_data.get('periodic_task'):
            periodic_task = validated_data.pop('periodic_task')

        if task_type == 'segmentation':
            segmentation_task = models.SegmentationTask.objects.create(
                **segment_data)

        task = models.Task.objects.create(**validated_data)

        if task_type == 'segmentation':
            task.segmentation_task = segmentation_task
            task.save()

        if periodic_task:
            crontab_str = periodic_task.pop('crontab')
            if crontab_str:
                crontab, _ = CrontabSchedule.objects.get_or_create(
                    minute=crontab_str.split(' ')[0],
                    hour=crontab_str.split(' ')[1],
                    day_of_week=crontab_str.split(' ')[2],
                    day_of_month=crontab_str.split(' ')[3],
                    month_of_year=crontab_str.split(' ')[4])
            task_kwargs = {
                'task_id': task.id,
                'request': None
            }
            if task.task_type == 'sync':
                task_name = 'plugin_mailchimp.tasks.sync'
            else:
                task_name = 'plugin_mailchimp.tasks.run_segmentation'

            periodic_task_object = PeriodicTask.objects.create(
                name='[Task] {}'.format(task.name),
                crontab=crontab,
                enabled=periodic_task.get('enabled'),
                task=task_name,
                kwargs=json.dumps(task_kwargs)
            )
            task.periodic_task = periodic_task_object
            task.save()
        task.refresh_from_db()
        return task

    def update(self, instance, validated_data):
        segmentation_task_data = validated_data.pop('segmentation_task')
        periodic_task = validated_data.pop('periodic_task')

        if validated_data['task_type'] == 'segmentation':
            segmentation_task = instance.segmentation_task
            models.SegmentationTask.objects.filter(
                pk=segmentation_task.pk).update(**segmentation_task_data)

        models.Task.objects.filter(pk=instance.pk).update(**validated_data)

        if periodic_task:
            crontab_str = periodic_task.get('crontab', None)
            if instance.task_type == 'sync':
                task_name = 'plugin_mailchimp.tasks.sync'
            else:
                task_name = 'plugin_mailchimp.tasks.run_segmentation'

            try:
                crontab, _ = CrontabSchedule.objects.get_or_create(
                    minute=crontab_str.split(' ')[0],
                    hour=crontab_str.split(' ')[1],
                    day_of_week=crontab_str.split(' ')[2],
                    day_of_month=crontab_str.split(' ')[3],
                    month_of_year=crontab_str.split(' ')[4])
            except:
                crontab = CrontabSchedule.objects.filter(
                    minute=crontab_str.split(' ')[0],
                    hour=crontab_str.split(' ')[1],
                    day_of_week=crontab_str.split(' ')[2],
                    day_of_month=crontab_str.split(' ')[3],
                    month_of_year=crontab_str.split(' ')[4])[0]

            task_kwargs = {
                'task_id': instance.id,
                'request': None
            }

            if instance.periodic_task:
                periodic_task_object = instance.periodic_task
                periodic_task_object.enabled = periodic_task.get('enabled')
                periodic_task_object.crontab = crontab
                periodic_task_object.kwargs = json.dumps(task_kwargs)
                periodic_task_object.task = task_name
                periodic_task_object.save()
            else:

                periodic_task_object = PeriodicTask.objects.create(
                    name='[Task] {}'.format(instance.name),
                    crontab=crontab,
                    enabled=periodic_task.get('enabled'),
                    task=task_name,
                    kwargs=json.dumps(task_kwargs)
                )
                instance.periodic_task = periodic_task_object
                instance.save()

        instance.refresh_from_db()
        return instance


class TaskResultListSerializer(serializers.ModelSerializer):
    user = OwnerSerializer(read_only=True)
    task = serializers.ReadOnlyField(source='task.name')
    url = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = models.TaskResult
        fields = [
            "url",
            "id",
            "name",
            "status",
            "task",
            "date_start",
            "duration",
            "user",
            "success",
        ]

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse(
                "plugin_mailchimp:task-results-detail",
                kwargs={"pk": obj.pk, "task_pk": obj.task.pk},
            )
        )

    def get_duration(self, obj):
        if obj.duration:
            return api_utils.pretty_time_delta(obj.duration.seconds)
        return ''


class TaskResultSerializer(serializers.ModelSerializer):
    user = OwnerSerializer(read_only=True)

    class Meta:
        model = models.TaskResult
        fields = [
            "id",
            "name",
            "status",
            "task",
            "date_start",
            "duration",
            "user",
            "success",
            "stats",
        ]
