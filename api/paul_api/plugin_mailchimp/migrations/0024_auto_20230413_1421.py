# Generated by Django 3.2.18 on 2023-04-13 11:21

from django.conf import settings
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plugin_mailchimp', '0023_auto_20220730_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Settings', 'verbose_name_plural': 'Settings'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='date_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date end'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='date_start',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date start'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='stats',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='stats'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='status',
            field=models.CharField(default='In progress', max_length=20, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='success',
            field=models.BooleanField(default=False, verbose_name='success'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plugin_mailchimp_taskresult_tasks', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
