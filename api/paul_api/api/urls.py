from django.urls import path, include

from rest_framework.schemas import get_schema_view
from rest_framework.authtoken import views as token_views

from rest_framework_nested import routers

from . import views
from django.views.generic import TemplateView


router = routers.DefaultRouter()

router.register(r"users", views.UserViewSet)
router.register(r"databases", views.DatabaseViewSet)
router.register(r"filters", views.FilterViewSet)
router.register(r"tables", views.TableViewSet, basename="table")
router.register(r"csv-imports", views.CsvImportViewSet)
router.register(r"charts", views.ChartViewSet)
router.register(r"cards", views.CardViewSet)

tables_router = routers.NestedSimpleRouter(router, "tables", lookup="table")
tables_router.register("entries", views.EntryViewSet, basename="table-entries")


urlpatterns = [
    path("api-token-auth/", token_views.obtain_auth_token),
    path(
        "openapi",
        get_schema_view(
            title="Paul OpenSchema",
            description="API for Paul",
            version="0.0.1",
            url="http://dev.api.paul.ro:8000/"
            # urlconf='api.urls'
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="api/swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    path("i18n/", include("django.conf.urls.i18n")),
    path("user/", views.UserView.as_view()),
    path("auth/", include('djoser.urls')),
    path("", include(router.urls)),
    path("", include(tables_router.urls)),
]
