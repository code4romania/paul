from django.contrib import admin
from plugin_mailchimp import models
# Register your models here.


@admin.register(models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "audiences_table_name",
        "audiences_stats_table_name",
        "audience_segments_table_name",
        "audience_members_table_name")


@admin.register(models.TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("date_start", "date_end", "duration", "user", "success")


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "task_type")
