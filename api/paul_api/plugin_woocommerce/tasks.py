from django.contrib.auth.models import User
from plugin_woocommerce import utils, models, serializers
from celery import shared_task
from django.utils import timezone


@shared_task
def sync(request, task_id):
    if hasattr(request, 'user'):
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username='paul-sync')

    settings = models.Settings.objects.last()
    task = models.Task.objects.get(pk=task_id)

    task_result = models.TaskResult.objects.create(
        user=user,
        task=task)

    KEY = settings.key
    SECRET = settings.secret
    ENDPOINT_URL = settings.endpoint_url
    TABLE_ABONAMENTE = settings.table_abonamente
    TABLE_COMENZI_COMPACT = settings.table_comenzi_compact
    TABLE_COMENZI_DETALIAT = settings.table_comenzi_detaliat
    TABLE_CLIENTI = settings.table_clienti
    # TABLE_NAME = settings.table_name

    success, stats = utils.run_sync(
        KEY,
        SECRET,
        ENDPOINT_URL,
        TABLE_ABONAMENTE,
        TABLE_CLIENTI,
        TABLE_COMENZI_DETALIAT,
        TABLE_COMENZI_COMPACT,
        )

    task_result.success = success
    task_result.stats = stats
    task_result.status = 'Finished'
    task_result.date_end = timezone.now()
    task_result.duration = task_result.date_end - task_result.date_start
    
    task_result.save()

    return task_result.id, task_result.success
