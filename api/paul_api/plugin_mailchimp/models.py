from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_q.models import (
    Schedule,
    Task as QTask,
)


from api.models import Filter, PluginTaskResult


class Settings(models.Model):
    """
    Description: Model Description
    """

    key = models.CharField(max_length=255, help_text="Mailchimp API Key")
    audiences_table_name = models.CharField(max_length=255, default="[mailchimp] Audiences")
    audiences_stats_table_name = models.CharField(max_length=255, default="[mailchimp] Audiences Stats")
    audience_segments_table_name = models.CharField(max_length=255, default="[mailchimp] Audience Segments")
    audience_members_table_name = models.CharField(max_length=255, default="[mailchimp] Audiences Members")
    segment_members_table_name = models.CharField(max_length=255, default="[mailchimp] Segments Members")
    audience_tags_table_name = models.CharField(max_length=255, default="[mailchimp] Audience Tags")
    created_on = models.DateTimeField(blank=True, null=False, editable=False, auto_now_add=timezone.now)

    class Meta:
        get_latest_by = "created_on"
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")


class SegmentationTask(models.Model):
    """
    Description: Model Description
    """

    filtered_view = models.ForeignKey(Filter, null=True, blank=True, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        pass


class Task(models.Model):
    """
    Description: Model Description
    """

    SYNC_TASK = "sync"
    SEGMENTATION_TASK = "segmentation"
    UPLOAD_TASK = "upload"
    TASK_TYPES = (
        (SYNC_TASK, _("Import data from Mailchimp")), 
        (SEGMENTATION_TASK, _("Send segmentation to Mailchimp")),
        (UPLOAD_TASK, _("Send contacts to Mailchimp (WIP/TODO)")),
    )

    name = models.CharField(max_length=255, null=True, blank=True)
    task_type = models.CharField(max_length=12, choices=TASK_TYPES, db_index=True)  # TODO: limit this field len

    segmentation_task = models.ForeignKey(SegmentationTask, null=True, blank=True, on_delete=models.CASCADE)

    last_edit_date = models.DateTimeField(auto_now=True)  # TODO: The last edit is wrongly updated on cron too
    last_run_date = models.DateTimeField(null=True)
    last_edit_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="mailchimp_tasks")

    async_task_id = models.CharField(default="", max_length=32, blank=True, null=False, editable=False)  # TODO
    schedule_enabled = models.BooleanField(default=False, db_index=True)
    schedule = models.ForeignKey(
        Schedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="mailchimp_tasks"
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    @staticmethod
    def delete_failed_async_tasks():
        total = QTask.objects.filter(success=False, attempt_count__gt=3).delete()
        return total


@receiver(post_delete, sender=Task)
def delete_schedule(sender, **kwargs):
    instance = kwargs.get("instance")
    if instance.schedule:
        instance.schedule.delete()
    # if instance.async_task_id:
    #     QTask.objects.filter(id=instance.async_task_id).delete()


class TaskResult(PluginTaskResult):
    """
    Description: Model Description
    """

    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE, related_name="task_results")


@receiver(post_save, sender=TaskResult)
def update_task_run_date(sender, instance, **kwargs):

    created = kwargs.get("created")
    if created:
        task = instance.task
        task.last_run_date = timezone.now()
        task.save()
