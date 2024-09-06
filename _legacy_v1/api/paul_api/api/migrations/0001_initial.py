# Generated by Django 3.1rc1 on 2020-08-20 15:19

from django.conf import settings
import django.contrib.postgres.fields
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Database",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Filter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "creation_date",
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
                ("last_edit_date", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Table",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(blank=True, null=True)),
                ("active", models.BooleanField(default=False)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("last_edit_date", models.DateTimeField(blank=True, null=True)),
                (
                    "database",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tables",
                        to="api.database",
                    ),
                ),
                (
                    "last_edit_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="last_table_edits",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": (
                    ("view", "View"),
                    ("change", "View"),
                    ("delete", "View"),
                ),
            },
        ),
        migrations.CreateModel(
            name="Userprofile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.UUIDField(default=uuid.uuid4)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TableColumn",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("int", "int"),
                            ("float", "float"),
                            ("text", "text"),
                            ("date", "date"),
                            ("bool", "bool"),
                            ("object", "object"),
                            ("enum", "enum"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "help_text",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "choices",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("required", models.BooleanField(default=False)),
                ("unique", models.BooleanField(default=False)),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="api.table",
                    ),
                ),
            ],
            options={
                "unique_together": {("table", "slug")},
            },
        ),
        migrations.CreateModel(
            name="FilterJoinTable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fields",
                    models.ManyToManyField(
                        related_name="filter_join_table_fields",
                        to="api.TableColumn",
                    ),
                ),
                (
                    "filter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="filter_join_tables",
                        to="api.filter",
                    ),
                ),
                (
                    "join_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.tablecolumn",
                    ),
                ),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.table",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="filter",
            name="join_field",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="filter_primary_table_join_field",
                to="api.tablecolumn",
            ),
        ),
        migrations.AddField(
            model_name="filter",
            name="join_tables",
            field=models.ManyToManyField(
                related_name="filter_join_table",
                through="api.FilterJoinTable",
                to="api.Table",
            ),
        ),
        migrations.AddField(
            model_name="filter",
            name="last_edit_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="last_filter_edits",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="filter",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="filter",
            name="primary_table",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="api.table"),
        ),
        migrations.AddField(
            model_name="filter",
            name="primary_table_fields",
            field=models.ManyToManyField(related_name="filter_primary_table_field", to="api.TableColumn"),
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "data",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="api.table",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Entries",
            },
        ),
    ]