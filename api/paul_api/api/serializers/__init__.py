from rest_framework import serializers

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from . import (
    users,
    databases,
    tables,
    filters,
    entries,
    charts,
    csvs,
    cards
    )


class WritableSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        super().__init__(**kwargs)

        self.read_only = False

    def get_default(self):
        default = super().get_default()

        return {
            self.field_name: default
        }

    def to_internal_value(self, data):
        return {self.field_name: data}


class TaskScheduleCrontabSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrontabSchedule
        fields = [
            "minute",
            "hour",
            "day_of_week",
            "day_of_month",
            "month_of_year"
        ]


class TaskScheduleSerializer(serializers.ModelSerializer):
    crontab = WritableSerializerMethodField()

    class Meta:
        model = PeriodicTask
        fields = [
            "enabled",
            "crontab"
        ]

    def get_crontab(self, obj):
        return '{} {} {} {} {}'.format(
            obj.crontab.minute,
            obj.crontab.hour,
            obj.crontab.day_of_week,
            obj.crontab.day_of_month,
            obj.crontab.month_of_year)
