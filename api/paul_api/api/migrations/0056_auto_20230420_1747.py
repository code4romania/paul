from django.db import migrations
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def delete_obsolete_table_permissions(apps, schema_editor):
    
    obsolete_codenames = ("view", "change", "delete")
    ct = ContentType.objects.get(app_label="api", model="table")

    Permission.objects.filter(
        content_type=ct, codename__in=obsolete_codenames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_alter_table_options'),
    ]

    operations = [
        migrations.RunPython(delete_obsolete_table_permissions)
    ]
