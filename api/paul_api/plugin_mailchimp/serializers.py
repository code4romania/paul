from django.urls import reverse
from django.utils import timezone
from django_q.models import Schedule
from rest_framework import serializers

from api import utils as api_utils
from api.serializers.users import OwnerSerializer
from api.serializers import TaskScheduleSerializer
from plugin_mailchimp.models import (
    Settings as MailchimpSettings,
    Task,
    SegmentationTask,
    TaskResult
)


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailchimpSettings
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
    crontab = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="plugin_mailchimp:task-detail")

    class Meta:
        model = Task
        fields = (
            "url",
            "id",
            "name",
            "schedule_enabled",
            "task_type",
            "crontab",
            "last_edit_date",
            "last_run_date",
            "last_edit_user",
        )

    def get_crontab(self, obj):
        if obj.schedule:
            return obj.schedule.cron
        return None


class SegmentationTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SegmentationTask
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
    schedule = TaskScheduleSerializer(required=False, allow_null=True)
    schedule_enabled = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "task_results",
            "task_type",
            "segmentation_task",
            "schedule",
            "schedule_enabled",
            "last_edit_date",
            "last_edit_user",
        ]

    def validate_schedule_enabled(self, value):
        if value is None:
            return False
        else:
            return bool(value)

    def get_task_results(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse(
                "plugin_mailchimp:task-results-list",
                kwargs={"task_pk": obj.pk}))


class TaskCreateSerializer(serializers.ModelSerializer):
    last_edit_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    last_edit_date = serializers.HiddenField(default=timezone.now)
    segmentation_task = SegmentationTaskSerializer(
        required=False, allow_null=True)
    schedule = TaskScheduleSerializer(required=False, allow_null=True)
    schedule_enabled = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "task_type",
            "segmentation_task",
            "last_edit_date",
            "last_edit_user",
            "schedule_enabled",
            "schedule",
        ]

    def validate_schedule_enabled(self, value):
        if value is None:
            return False
        else:
            return bool(value)

    def create(self, validated_data):
        task_type = validated_data['task_type']
        segment_data = validated_data.pop('segmentation_task')
        schedule = None

        if validated_data.get('schedule'):
            schedule = validated_data.pop('schedule')

        if task_type == 'segmentation':
            segmentation_task = SegmentationTask.objects.create(
                **segment_data
            )

        task = Task.objects.create(**validated_data)

        if task_type == 'segmentation':
            task.segmentation_task = segmentation_task
            task.save()

        if schedule and validated_data.get('schedule_enabled'):
            task_args = "{},{}".format(0, task.pk)

            if task.task_type == 'sync':
                task_name = 'plugin_mailchimp.tasks.run_sync'
            else:
                task_name = 'plugin_mailchimp.tasks.run_segmentation'

            task_schedule = Schedule.objects.create(
                name='[Task] {}'.format(task.name),
                cron=schedule.get("cron"),
                schedule_type=Schedule.CRON,
                func=task_name,
                args=task_args,
            )
            task.schedule = task_schedule
            task.save()
        task.refresh_from_db()
        return task

    def update(self, instance, validated_data):
        segmentation_task_data = validated_data.pop('segmentation_task')
        schedule = validated_data.pop('schedule')

        if validated_data['task_type'] == 'segmentation':
            segmentation_task = instance.segmentation_task
            SegmentationTask.objects.filter(
                pk=segmentation_task.pk).update(**segmentation_task_data)

        Task.objects.filter(pk=instance.pk).update(**validated_data)

        if validated_data.get("schedule_enabled"):
            crontab_str = schedule.get('cron', None)
            if instance.task_type == 'sync':
                task_name = 'plugin_mailchimp.tasks.run_sync'
            else:
                task_name = 'plugin_mailchimp.tasks.run_segmentation'

            task_args = "{},{}".format(0, instance.pk)

            if instance.schedule:
                task_schedule = instance.schedule
                task_schedule.cron = crontab_str
                task_schedule.args = task_args
                task_schedule.task = task_name
                task_schedule.save()
            else:
                task_schedule = Schedule.objects.create(
                    name='[Task] {}'.format(instance.name),
                    cron=crontab_str,
                    schedule_type=Schedule.CRON,
                    func=task_name,
                    args=task_args,
                )
                instance.schedule = task_schedule
                instance.schedule_enabled = True
                instance.save()
        elif instance.schedule:
            instance.schedule_enabled = False
            instance.schedule.delete()

        instance.refresh_from_db()
        return instance


class TaskResultListSerializer(serializers.ModelSerializer):
    user = OwnerSerializer(read_only=True)
    task = serializers.ReadOnlyField(source='task.name')
    url = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = TaskResult
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
        model = TaskResult
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
