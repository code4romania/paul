from django.contrib import admin
from plugin_woocommerce import models
# Register your models here.


@admin.register(models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "secret", "endpoint_url")


@admin.register(models.TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("date_start", "date_end", "duration", "user", "success")


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "task_type")
