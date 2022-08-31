"""paul_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


plugin_urlpatterns = []

if settings.PLUGIN_MAILCHIMP_ENABLED:
    plugin_urlpatterns.append(
        path(
            "api/mailchimp/",
            include("plugin_mailchimp.urls", namespace="plugin_mailchimp"),
        )
    )

if settings.PLUGIN_WOOCOMMERCE_ENABLED:
    plugin_urlpatterns.append(
        path(
            "api/woocommerce/",
            include("plugin_woocommerce.urls", namespace="plugin_woocommerce"),
        )
    )


urlpatterns = (
    i18n_patterns(
        path("api/api-token-auth/", include("rest_framework.urls")),
        path("api/admin/", admin.site.urls),
        # path("api/silk/", include("silk.urls", namespace="silk")),
        *plugin_urlpatterns,
        path("api/", include("api.urls")),
    )
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
