# Generated by Django 3.1.2 on 2020-10-06 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plugin_woocommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskresult',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='woocommerce_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]