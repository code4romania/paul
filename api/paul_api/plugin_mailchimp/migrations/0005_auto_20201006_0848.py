# Generated by Django 3.1.2 on 2020-10-06 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plugin_mailchimp', '0004_auto_20201006_0846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settings',
            old_name='audiences_members_table_name',
            new_name='audience_members_table_name',
        ),
        migrations.RenameField(
            model_name='settings',
            old_name='audience_table_name',
            new_name='audiences_table_name',
        ),
    ]
