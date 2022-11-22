from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from api import models


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