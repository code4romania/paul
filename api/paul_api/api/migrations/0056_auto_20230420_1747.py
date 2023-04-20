from django.db import migrations


def delete_obsolete_table_permissions(apps, schema_editor):
    obsolete_codenames = ("view", "change", "delete")

    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")

    try:
        ct = ContentType.objects.get(app_label="api", model="table")
    except ContentType.DoesNotExist:
        pass
    else:
        Permission.objects.filter(
            content_type=ct, codename__in=obsolete_codenames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_alter_table_options'),
    ]

    operations = [
        migrations.RunPython(delete_obsolete_table_permissions)
    ]
