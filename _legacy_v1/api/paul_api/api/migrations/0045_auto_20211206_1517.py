# Generated by Django 3.2.9 on 2021-12-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20210129_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvfieldmap',
            name='required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='csvfieldmap',
            name='unique',
            field=models.BooleanField(default=False),
        ),
    ]