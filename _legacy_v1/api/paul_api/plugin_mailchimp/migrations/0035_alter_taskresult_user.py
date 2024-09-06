# Generated by Django 4.2.1 on 2023-06-23 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plugin_mailchimp', '0034_update_contacts_data_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskresult',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_tasks', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]