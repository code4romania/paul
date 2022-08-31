import random
from faker import Faker

from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware

from api import models
from django.utils.text import slugify
from datetime import datetime, timedelta
import json

fake = Faker()

datatypes = {
    "int": "int",
    "float": "float",
    "text": "text",
    "date": "date",
    "bool": "bool",
    "enum": "enum",
}


def gen_slug(value):
    return slugify(value).replace("-", "_")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        db, _ = models.Database.objects.get_or_create(name="DOR")
        admin_group, _ = Group.objects.get_or_create(name="admin")
        admin, _ = User.objects.get_or_create(username="admin")
        admin.set_password("admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.groups.add(admin_group)
        admin.save()
        try:
            print(admin.userprofile)
        except:
            profile = models.Userprofile(user=admin)
            profile.save()

        tables = {}
        tables_map = {
            "Utilizatori": {
                "nume": "text",
                "prenume": "text",
                "email": "text",
                "data_nasterii": "date",
                "telefon": "text",
                "activ": "bool",
                "sex": "enum",
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
        # print(models.Table.objects.all().delete())
        # print(models.Entry.objects.all().delete())
        for table_name in tables_map.keys():
            tables[table_name], _ = models.Table.objects.get_or_create(
                database=db, name=table_name.capitalize(), owner=admin
            )

        for table in models.Table.objects.all():
            print("Deleting all columns from table", table)
            print(table.fields.all().delete())
            print("Deleting all entries from table", table)
            print(table.entries.all().delete())
        for table_name, fields in tables_map.items():
            table = models.Table.objects.get(name=table_name)
            table.active = True
            table.save()
            for field_name, field_type in fields.items():
                print("create field {} in table {}".format(field_name, table))
                if field_type == "enum":
                    column = models.TableColumn.objects.get_or_create(
                        table=table,
                        name=gen_slug(field_name),
                        field_type=field_type,
                        choices=["M", "F"],
                        display_name=field_name.replace("_", " ").title(),
                    )
                else:
                    column = models.TableColumn.objects.get_or_create(
                        table=table,
                        name=gen_slug(field_name),
                        field_type=field_type,
                        display_name=field_name.replace("_", " ").title(),
                    )

        utilizatori = models.Table.objects.get(name="Utilizatori")
        evenimente = models.Table.objects.get(name="Evenimente")
        abonamente = models.Table.objects.get(name="Abonamente")
        entries = []
        # last_id = models.Entry.objects.last().pk if models.Entry.objects.last() else 1
        for i in range(10000):
            entry = models.Entry(table=utilizatori)
            data = {}
            data["nume"] = fake.name().split(" ")[1]
            data["prenume"] = fake.name().split(" ")[0]
            data["email"] = fake.email()
            d = datetime.combine(fake.date_of_birth(), datetime.min.time()) + timedelta(hours=9)
            data["data_nasterii"] = make_aware(d)
            data["telefon"] = fake.phone_number()
            data["activ"] = random.choice([True, False])
            data["sex"] = random.choice(["M", "F"])
            # entry.data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
            entry.data = data
            entries.append(entry)
            # entry.save()

            abonamente_count = 0
            evenimente_count = 0
            for ii in range(random.choice([0, 2, 3, 5])):
                abonamente_count += 1
                abonament = models.Entry(table=abonamente)
                data = {}
                data["email"] = entry.data["email"]
                data["nume"] = entry.data["nume"]
                data["prenume"] = entry.data["prenume"]
                d = datetime.combine(fake.date_of_birth(), datetime.min.time()) + timedelta(hours=6)
                data["data"] = make_aware(d)
                data["pret"] = random.choice([100, 200, 150, 120])
                data["tip"] = random.choice(["Abonament digital", "Revista"])
                # abonament.data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
                abonament.data = data
                # abonament.save()
                entries.append(abonament)
            for iii in range(random.choice([0, 2, 3, 5])):
                evenimente_count += 1
                eveniment = models.Entry(table=evenimente)
                data = {}
                data["denumire"] = random.choice(["DOR Live", "Power of Storytelling", "DOR online"])
                data["email"] = entry.data["email"]
                d = datetime.combine(fake.date_of_birth(), datetime.min.time()) + timedelta(hours=6)
                data["data"] = make_aware(d)
                data["pret"] = random.choice([100, 200, 150, 120])
                data["oras"] = random.choice(["Arad", "Timisoara", "Oradea", "Cluj", "Bucuresti"])
                # eveniment.data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
                eveniment.data = data
                # eveniment.save()
                entries.append(eveniment)
            # print(entry.data)
            # print(entry.data['nume'])
            print(
                "{}. Create user {} {} ({} abonamente | {} evenimente)".format(
                    i,
                    entry.data["nume"],
                    entry.data["prenume"],
                    abonamente_count,
                    evenimente_count,
                )
            )

            if i % 10000 == 0:
                print("Saving batch {}".format(i / 10000))
                models.Entry.objects.bulk_create(entries)
                print("Batch {} saved".format(i / 10000))
                entries = []
        print("Saving batch {}".format(i / 10000))
        models.Entry.objects.bulk_create(entries)
        print("Batch {} saved".format(i / 10000))


# fake.text()
# random.choice([3, 4, 5, 6, 10])
# fake.date_between(start_date="-30y", end_date="today"),
