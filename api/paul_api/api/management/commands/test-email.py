import random
from faker import Faker

from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware

from api import models, utils
from django.utils.text import slugify
from datetime import datetime, timedelta
import json



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admins = User.objects.filter(groups__name='admin')
        user = User.objects.last()
        base_path = 'http://localhost:8080'

        for admin in admins:
            utils.send_email(
                template="mail/new_user.html",
                context={"admin": admin, "user": user, "base_path": base_path},
                subject="[PAUL] New user registered",
                to=admin.email)
