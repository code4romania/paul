# Generated by Django 3.1.2 on 2020-10-06 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plugin_mailchimp', '0005_auto_20201006_0848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskresult',
            old_name='errors',
            new_name='stats',
        ),
        migrations.RemoveField(
            model_name='taskresult',
            name='updates',
        ),
    ]
