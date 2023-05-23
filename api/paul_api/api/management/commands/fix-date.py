from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from api import models


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
