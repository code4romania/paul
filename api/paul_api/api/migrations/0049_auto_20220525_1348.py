# Generated by Django 3.2.9 on 2022-05-25 13:48

from django.db import migrations
from django.contrib.sites.models import Site
from django.conf import settings

def forwards_func(apps, schema_editor):

    # site = Site.objects.last()
    # site.domain = settings.FRONTEND_DOMAIN
    # site.name = settings.FRONTEND_DOMAIN
    # site.save()
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20220525_1322'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
