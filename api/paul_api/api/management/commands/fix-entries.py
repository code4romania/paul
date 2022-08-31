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
        i = 0
        c = models.Entry.objects.count()
        for entry in models.Entry.objects.all().prefetch_related('table').order_by('-table__id'):
            i += 1
            try:
                entry.clean_fields()

                entry.save()
            except Exception as e:
                print(e)
            print(i, c, entry.table)