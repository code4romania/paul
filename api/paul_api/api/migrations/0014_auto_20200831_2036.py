# Generated by Django 3.1 on 2020-08-31 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_auto_20200831_2035"),
    ]

    operations = [
        migrations.AlterField(
            model_name="csvimport",
            name="imports_count",
            field=models.IntegerField(default=0),
        ),
    ]
