from typing import Callable
from inertia import share

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse

from users.models import User


def global_state(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    """
    Properties made available to every request response
    """

    def extract_messages(request: HttpRequest) -> list[dict]:
        """
        Extract flash messages from the session storage
        """
        messages = []
        for message in get_messages(request):
            messages.append(
                {
                    "message": message.message,
                    "level_tag": message.level_tag,
                }
            )
        return messages

    def middleware(request: HttpRequest) -> HttpResponse:
        """
        Inject some global data into each HttpResponse
        """
        share(
            request=request,
            # Computed properties:
            flash_messages=extract_messages(request),
            # Lazily computed properties:
            is_authenticated=lambda: request.user.is_authenticated,
            user=lambda: User.to_dict(request.user) if request.user.is_authenticated else None,
        )
        return get_response(request)

    return middleware
