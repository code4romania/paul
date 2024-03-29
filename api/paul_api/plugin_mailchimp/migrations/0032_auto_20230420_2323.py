# Generated by Django 3.2.18 on 2023-04-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugin_mailchimp', '0031_alter_task_async_task_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='async_task_id',
        ),
        migrations.AlterField(
            model_name='task',
            name='last_edit_date',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_run_date',
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
