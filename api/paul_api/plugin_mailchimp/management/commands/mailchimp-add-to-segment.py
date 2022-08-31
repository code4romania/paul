from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware
from django.http import HttpRequest

from plugin_mailchimp import models, tasks, utils, serializers
from django.utils.text import slugify
from datetime import datetime, timedelta

from pprint import pprint



from rest_framework.request import Request
from rest_framework.test import force_authenticate, APIRequestFactory

from api import views
from django.test import RequestFactory

import requests
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # print('add to segment mailchimp')
        url = 'http://api:8000/api/filters/58/'
        # r = requests.get(url)
        # print(r.json())
        print(tasks.run_segmentation(None, 22))