from rest_framework import viewsets, mixins, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from plugin_woocommerce import (
    models,
    serializers,
    tasks)
from api.views import EntriesPagination


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    pagination_class = EntriesPagination
    filter_backends = (filters.OrderingFilter,)

    ordering_fields = {
        'name': 'name',
        'task_type': 'task_type',
        'last_edit_date': 'last_edit_date',
        'last_run_date': 'last_run_date',
        'schedule_enabled': 'periodic_task__enabled',
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

        if task.task_type == 'sync':
            print('aici')
            # tasks.sync.apply_async(args=[None, task.id])
            task_result_id = tasks.sync.apply_async(args=[None, task.id])
            print(task_result_id)
        else:
            task_result_id, _ = tasks.run_segmentation(request, task.id)

        # task_result = models.TaskResult.objects.get(pk=task_result_id)
        # result = serializers.TaskResultSerializer(
            # task_result, context={'request': request})
        result = {'data': {}}
        return Response(result)


    @action(
        detail=True,
        methods=["get"],
        name="Run Task",
        url_path="run",
    )
    def run(self, request, pk):
        task = self.get_object()
        if task.task_type == 'sync':
            # task_result_id  = tasks.sync(request, task.pk)
            task_result_id = tasks.sync.apply_async(args=[None, task.id])
            # task_result = models.TaskResult.objects.get(pk=task_result_id)

        result = {'data': {}}
        return Response(result)


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TaskResult.objects.all()
    pagination_class = EntriesPagination
    filter_backends = (filters.OrderingFilter,)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.TaskResultListSerializer
        return serializers.TaskResultSerializer

    def get_queryset(self):
        return models.TaskResult.objects.filter(task=self.kwargs["task_pk"])


class SettingsViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.Settings.objects.all()
    serializer_class = serializers.SettingsSerializer



