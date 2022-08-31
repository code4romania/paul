import random
from faker import Faker

from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware
from eav.models import Attribute
from api import models
from django.utils.text import slugify
from datetime import datetime, timedelta

fake = Faker()

datatypes = {
    "int": Attribute.TYPE_INT,
    "float": Attribute.TYPE_FLOAT,
    "text": Attribute.TYPE_TEXT,
    "date": Attribute.TYPE_DATE,
    "bool": Attribute.TYPE_BOOLEAN,
    "object": Attribute.TYPE_OBJECT,
    "enum": Attribute.TYPE_ENUM,
}


def gen_slug(value):
    return slugify(value).replace("-", "_")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        db, _ = models.Database.objects.get_or_create(name="DOR")
        admin, _ = User.objects.get_or_create(username="admin")
        tables = {}
        tables_map = {
            "Utilizatori": {
                "nume": "text",
                "prenume": "text",
                "email": "text",
                "data_nasterii": "date",
                "telefon": "text",
                "activ": "bool",
            },
            "Evenimente": {
                "denumire": "text",
                "email": "text",
                "data": "date",
                "pret": "float",
                "oras": "text",
            },
            "Abonamente": {
                "email": "text",
                "nume": "text",
                "prenume": "text",
                "data": "date",
                "pret": "float",
                "tip": "text",
            },
        }
        print(models.Table.objects.all().delete())
        for table_name in tables_map.keys():
            tables[table_name], _ = models.Table.objects.get_or_create(
                database=db, name=table_name.capitalize(), owner=admin
            )

        for table in models.Table.objects.all():
            print("Deleting all columns from table", table)
            print(table.fields.all().delete())
            print("Deleting all entries from table", table)
            print(table.entries.all().delete())
        print("Delete all attributes", Attribute.objects.all().delete())
        for table_name, fields in tables_map.items():
            table = models.Table.objects.get(name=table_name)
            for field_name, field_type in fields.items():
                print("create field {} in table {}".format(field_name, table))
                column = models.TableColumn.objects.get_or_create(
                    table=table,
                    name=gen_slug(field_name),
                    field_type=field_type,
                )
                Attribute.objects.get_or_create(
                    name=field_name,
                    slug=gen_slug(field_name),
                    datatype=datatypes[field_type],
                )

        utilizatori = models.Table.objects.get(name="Utilizatori")
        evenimente = models.Table.objects.get(name="Evenimente")
        abonamente = models.Table.objects.get(name="Abonamente")
        entries = []
        for i in range(1000):
            entry = models.Entry.objects.create(table=utilizatori)
            entry.eav.nume = fake.name().split(" ")[1]
            entry.eav.prenume = fake.name().split(" ")[0]
            entry.eav.email = fake.email()
            d = datetime.combine(fake.date_of_birth(), datetime.min.time()) + timedelta(hours=6)
            entry.eav.data_nasterii = make_aware(d)
            entry.eav.telefon = fake.phone_number()
            entry.eav.activ = random.choice([True, False])
            # entries.append(entry)
            entry.save()

            abonamente_count = 0
            evenimente_count = 0
            for ii in range(random.choice([0, 2, 3, 5])):
                abonamente_count += 1
                abonament = models.Entry.objects.create(table=abonamente)
                abonament.eav.email = entry.eav.email
                abonament.eav.nume = entry.eav.nume
                abonament.eav.prenume = entry.eav.prenume
                d = datetime.combine(fake.date_of_birth(), datetime.min.time()) + timedelta(hours=6)
                abonament.eav.data = make_aware(d)
                abonament.eav.pret = random.choice([100, 200, 150, 120])
                abonament.eav.tip = random.choice(["Abonament digital", "Revista"])
                abonament.save()
                # entries.append(abonament)
            for iii in range(random.choice([0, 2, 3, 5])):
                evenimente_count += 1
                eveniment = models.Entry.objects.create(table=evenimente)
                eveniment.eav.denumire = random.choice(["DOR Live", "Power of Storytelling", "DOR online"])
                eveniment.eav.email = entry.eav.email
                d = datetime.combine(fake.date_of_birth(), datetime.min.time()) + timedelta(hours=6)
                eveniment.eav.data = make_aware(d)
                eveniment.eav.pret = random.choice([100, 200, 150, 120])
                eveniment.eav.oras = random.choice(["Arad", "Timisoara", "Oradea", "Cluj", "Bucuresti"])

                eveniment.save()
                # entries.append(eveniment)
            print(
                "{}. Created user {} {} ({} abonamente | {} evenimente)".format(
                    i,
                    entry.eav.nume,
                    entry.eav.prenume,
                    abonamente_count,
                    evenimente_count,
                )
            )
        models.Entry.objects.bulk_create(entries)


# fake.text()
# random.choice([3, 4, 5, 6, 10])
# fake.date_between(start_date="-30y", end_date="today"),
