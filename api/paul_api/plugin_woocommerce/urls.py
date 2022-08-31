from django.urls import path, include

from rest_framework_nested import routers

from plugin_woocommerce import views

app_name = 'plugin_woocommerce'

router = routers.DefaultRouter()

router.register(r"settings", views.SettingsViewSet)
router.register(r"tasks", views.TaskViewSet, basename="task")

tasks_router = routers.NestedSimpleRouter(router, "tasks", lookup="task")
tasks_router.register("task-results", views.TaskResultViewSet, basename="task-results")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(tasks_router.urls)),
]
