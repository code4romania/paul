from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_control, never_cache


@cache_control(private=False)
def home(request: HttpRequest) -> HttpResponse:
    """
    Public homepage
    """
    return render(request, "hello/home.html", {})


@never_cache
def health(request: HttpRequest) -> HttpResponse:
    """
    Health check endpoint
    """
    normal_response_text = f"OK - {timezone.now()}"

    # Show detailed information only to authenticated staff members
    if request.user.is_authenticated and (
        request.user.is_staff
        or request.user.is_superuser
        or request.user.is_admin_member
        or request.user.is_superadmin_member
    ):
        return HttpResponse(
            f"{normal_response_text} [user #{request.user.pk}] [{settings.VERSION} {settings.REVISION}]"
        )

    return HttpResponse(normal_response_text)
