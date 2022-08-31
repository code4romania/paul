from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware
from django.http import HttpRequest

from plugin_mailchimp import models, tasks
from django.utils.text import slugify
from datetime import datetime, timedelta

from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('sync mailchimp')
        request = HttpRequest()
        request.method = 'GET'
        request.META['SERVER_NAME'] = 'dev.api.paul.ro'
        request.META['SERVER_PORT'] = '8000'

        response = tasks.sync(request, 7)
        pprint(response)
