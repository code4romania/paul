from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
import csv
from api import models
from eav.models import Attribute


def gen_slug(value):
    return slugify(value).replace("-", "_")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open("data/users.csv", "r") as f:
            csvfile = csv.DictReader(f, delimiter=";", quoting=csv.QUOTE_NONE)
            table_name = f.name.split("/")[-1].split(".")[0]
            admin = User.objects.get(username="admin")
            db, _ = models.Database.objects.get_or_create(name="DOR")
            table, _ = models.Table.objects.get_or_create(database=db, name=table_name.capitalize(), owner=admin)

            print("Deleting all columns from table", table)
            print(table.fields.all().delete())
            print("Deleting all entries from table", table)
            print(table.entries.all().delete())

            for field_name in csvfile.fieldnames:
                column = models.TableColumn.objects.get_or_create(
                    table=table, name=gen_slug(field_name), field_type="text"
                )
                Attribute.objects.get_or_create(
                    name=field_name,
                    slug=gen_slug(field_name),
                    datatype=Attribute.TYPE_TEXT,
                )

            for row in csvfile:
                print(row)
                entry = models.Entry.objects.create(table=table)
                for field, value in row.items():
                    print(" set {} to {}".format(gen_slug(field), value))
                    setattr(entry.eav, gen_slug(field), value)
                entry.save()
