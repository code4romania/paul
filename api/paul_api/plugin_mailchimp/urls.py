from django.urls import path, include

from rest_framework_nested import routers

from plugin_mailchimp import views

app_name = 'plugin_mailchimp'

router = routers.DefaultRouter()

router.register(r"settings", views.SettingsViewSet)
router.register(r"tasks", views.TaskViewSet)

tasks_router = routers.NestedSimpleRouter(router, "tasks", lookup="task")
tasks_router.register("task-results", views.TaskResultViewSet, basename="task-results")


urlpatterns = [
    path("get-audiences", views.AudiencesView.as_view()),
    path("", include(router.urls)),
    path("", include(tasks_router.urls)),
]
