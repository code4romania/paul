# Generated by Django 3.1.4 on 2020-12-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugin_woocommerce', '0010_auto_20201125_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='last_run_date',
            field=models.DateTimeField(null=True),
        ),
    ]