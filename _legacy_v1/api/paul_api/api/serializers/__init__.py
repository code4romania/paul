from rest_framework import serializers

from django_q.models import Schedule

from . import users, databases, tables, tablelinks, filters, entries, charts, csvs, cards


class WritableSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        super().__init__(**kwargs)

        self.read_only = False

    def get_default(self):
        default = super().get_default()

        return {self.field_name: default}

    def to_internal_value(self, data):
        return {self.field_name: data}


class TaskScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("cron",)
