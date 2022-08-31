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

from plugin_woocommerce import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Settings
        fields = [
            "key",
            "secret",
            "endpoint_url",
            "table_abonamente",
            "table_comenzi_compact",
            "table_comenzi_detaliat",
            "table_clienti",
        ]


class TaskListSerializer(serializers.ModelSerializer):
    last_edit_user = OwnerSerializer(read_only=True)
    schedule_enabled = serializers.SerializerMethodField()
    crontab = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="plugin_woocommerce:task-detail")

    class Meta:
        model = models.Task
        fields = [
            "url",
            "id",
            "name",
            "schedule_enabled",
            "crontab",
            "task_type",
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


class TaskSerializer(serializers.ModelSerializer):
    last_edit_user = OwnerSerializer(read_only=True)
    task_results = serializers.SerializerMethodField()
    periodic_task = TaskScheduleSerializer()
    schedule_enabled = serializers.SerializerMethodField()

    class Meta:
        model = models.Task
        fields = [
            "id",
            "name",
            "schedule_enabled",
            "periodic_task",
            "task_results",
            "task_type",
            "last_edit_date",
            "last_edit_user",
        ]

    def get_task_results(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse("plugin_woocommerce:task-results-list",
                kwargs={"task_pk": obj.pk}))


    def get_schedule_enabled(self, obj):
        if obj.periodic_task:
            return obj.periodic_task.enabled
        return False


class TaskCreateSerializer(serializers.ModelSerializer):
    last_edit_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    last_edit_date = serializers.HiddenField(default=timezone.now())
    periodic_task = TaskScheduleSerializer(required=False)

    class Meta:
        model = models.Task
        fields = [
            "id",
            "name",
            "task_type",
            "last_edit_date",
            "last_edit_user",
            "periodic_task"
        ]

    def create(self, validated_data):
        task_type = validated_data['task_type']
        periodic_task = None

        if validated_data.get('periodic_task'):
            periodic_task = validated_data.pop('periodic_task')

        task = models.Task.objects.create(**validated_data)

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
            task_name = 'plugin_woocommerce.tasks.sync'
         
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
        periodic_task = validated_data.pop('periodic_task')

        models.Task.objects.filter(pk=instance.pk).update(**validated_data)

        if periodic_task:
            crontab_str = periodic_task.get('crontab', None)
            if instance.task_type == 'sync':
                task_name = 'plugin_woocommerce.tasks.sync'

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
                "plugin_woocommerce:task-results-detail",
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
