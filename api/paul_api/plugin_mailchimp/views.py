from django_q.tasks import async_task
from rest_framework import viewsets, mixins
from rest_framework_tricks import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from api.views import EntriesPagination
from api.models import Entry
from plugin_mailchimp import serializers
from plugin_mailchimp.models import (
    Task, 
    TaskResult, 
    Settings as MailchimpSettings,
)



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-last_edit_date")
    pagination_class = EntriesPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = {
        'name': 'name',
        'task_type': 'task_type',
        'last_edit_date': 'last_edit_date',
        'last_run_date': 'last_run_date',
        'last_edit_user.username': 'last_edit_user__username',
    }

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.TaskListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return serializers.TaskCreateSerializer
        return serializers.TaskSerializer

    @action(
        detail=True,
        methods=["get"],
        name="Run Task",
        url_path="run",
    )
    def run(self, request, pk):
        task = self.get_object()

        if task.task_type == Task.SEGMENTATION_TASK:
            task_name = 'plugin_mailchimp.tasks.run_segmentation'
        elif task.task_type == Task.UPLOAD_TASK:
            task_name = 'plugin_mailchimp.tasks.run_contacts_to_mailchimp'
        elif task.task_type == Task.SYNC_TASK:
            task_name = 'plugin_mailchimp.tasks.run_sync'
        else:
            task_name = ""

        if task_name:
            async_task(task_name, request.user.id, task.id)

        result = {'data': {}}
        return Response(result)


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = EntriesPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = {
        'user.username': 'user__username',
        'duration': 'duration',
        'status': 'status',
        'date_start': 'date_start',
        'success': 'success',
    }

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.TaskResultListSerializer
        return serializers.TaskResultSerializer

    def get_queryset(self):
        return TaskResult.objects.filter(
            task=self.kwargs.get("task_pk", 0)
        ).order_by('-date_start')


class SettingsViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    
    queryset = MailchimpSettings.objects.all()
    serializer_class = serializers.SettingsSerializer


class AudiencesView(APIView):
    """
    View that runs the mailchimp sync
    """

    def get(self, request, format=None):
        settings = MailchimpSettings.objects.latest()
        audiences = Entry.objects.filter(
            table__name=settings.audiences_table_name).values(
            'data__id', 'data__name')
        tags = Entry.objects.filter(
            table__name=settings.audience_tags_table_name).values(
            'data__id', 'data__name', 'data__audience_id')
        response = []
        for audience in audiences:
            audience_dict = {
                "name": audience['data__name'],
                "id": audience['data__id'],
                "tags": []
            }
            audience_tags = list(
                filter(lambda x: x['data__audience_id'] == audience_dict['id'], tags)
            )

            for tag in audience_tags:
                audience_dict['tags'].append(tag['data__name'])
            response.append(audience_dict)
        return Response(response)
