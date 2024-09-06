# Generated by Django 3.2.18 on 2023-04-19 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugin_mailchimp', '0027_rename_periodic_task_enabled_task_schedule_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('sync', 'Import data from Mailchimp'), ('segmentation', 'Send segmentation to Mailchimp'), ('upload', 'Send contacts to Mailchimp (WIP/TODO)')], db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='status',
            field=models.CharField(choices=[('In progress', 'In progress'), ('Finished', 'Finished')], db_index=True, default='In progress', max_length=11, verbose_name='status'),
        ),
    ]