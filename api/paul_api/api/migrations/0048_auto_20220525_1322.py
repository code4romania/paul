# Generated by Django 3.2.9 on 2022-05-25 13:22

from django.db import migrations
from django.contrib.auth.models import Group, User
from api.models import Userprofile


def forwards_func(apps, schema_editor):

    for user in User.objects.all():
        Userprofile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20220525_1218'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
