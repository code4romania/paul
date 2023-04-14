# Generated by Django 3.2.18 on 2023-04-14 12:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plugin_mailchimp', '0024_auto_20230413_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='settings',
            name='key',
            field=models.CharField(help_text='Mailchimp API Key', max_length=255),
        ),
    ]
