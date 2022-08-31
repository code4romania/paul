from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware
from django.http import HttpRequest

from plugin_woocommerce import utils, models, tasks
from django.utils.text import slugify
from datetime import datetime, timedelta

from pprint import pprint



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # print('sync woocommerce')
        # ENDPOINT_URL = "https://dor.ro/wp-json/wc/"
        # KEY = "ck_dfeab47b910ef6b5113cadc93d27b51cfff357b3"
        # SECRET = "cs_2a6077c83243eb84fe9b788668b29d62e9b82d40"
        # r = utils.main(
        #     KEY,
        #     SECRET,
        #     ENDPOINT_URL
        #     )
        # print(r)

        # user, _ = User.objects.get_or_create(username='paul-sync')

        # settings = models.Settings.objects.last()
        # task = models.Task.objects.last()

        # task_result = models.TaskResult.objects.create(
        #     user=user,
        #     task=task)

        # KEY = settings.key
        # SECRET = settings.secret
        # ENDPOINT_URL = settings.endpoint_url
        # TABLE_ABONAMENTE = settings.table_abonamente
        # TABLE_COMENZI_COMPACT = settings.table_comenzi_compact
        # TABLE_COMENZI_DETALIAT = settings.table_comenzi_detaliat
        # TABLE_CLIENTI = settings.table_clienti
        # # TABLE_NAME = settings.table_name

        # success, stats = utils.run_sync(
        #     KEY,
        #     SECRET,
        #     ENDPOINT_URL,
        #     TABLE_ABONAMENTE,
        #     TABLE_CLIENTI,
        #     TABLE_COMENZI_DETALIAT,
        #     TABLE_COMENZI_COMPACT,
        #     )

        # task_result.success = success
        # task_result.stats = stats
        # task_result.status = 'Finished'
        # task_result.save()


        request = HttpRequest()
        request.method = 'GET'
        request.META['SERVER_NAME'] = 'dev.api.paul.ro'
        request.META['SERVER_PORT'] = '8000'
        last_task = models.Task.objects.last()
        print(last_task)
        response = tasks.sync(request, last_task.id)
        pprint(response)