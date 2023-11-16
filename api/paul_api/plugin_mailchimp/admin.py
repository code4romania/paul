from django.contrib import admin

from plugin_mailchimp.models import Settings as MailchimpSettings, Task, TaskResult


@admin.register(MailchimpSettings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "audiences_table_name",
        "audiences_stats_table_name",
        "audience_segments_table_name",
        "audience_members_table_name",
    )


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("date_start", "date_end", "duration", "user", "success")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "task_type")
