from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from api import utils


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admins = User.objects.filter(groups__name="admin")
        user = User.objects.last()
        base_path = "http://localhost:8080"

        for admin in admins:
            utils.send_email(
                template="email/new_user.html",
                context={"admin": admin, "user": user, "base_path": base_path},
                subject="[PAUL] New user registered",
                to=admin.email,
            )
