from django.db import migrations


def create_user_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name="user")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_auto_20230420_1747'),
    ]

    operations = [
        migrations.RunPython(create_user_group),
    ]
