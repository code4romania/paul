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
        for table in models.Table.objects.all():
            date_fields = []
            print('---', table)

            for field in table.fields.filter(field_type="date"):
                print(field.name)
                date_fields.append(field.name)
            i = 0
            for entry in table.entries.all():
                i += 1
                print(i, table)
                for field in date_fields:
                    try:
                        entry.data[field] = entry.data[field][:10]
                    except:
                        print('****errr:', entry.data)
                entry.save()
