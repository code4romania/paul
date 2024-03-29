# Generated by Django 3.2.14 on 2022-11-18 12:33

from django.conf import settings
import django.contrib.postgres.fields
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0052_userprofile_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csvfieldmap',
            options={'verbose_name': 'CSV field map', 'verbose_name_plural': 'CSV field maps'},
        ),
        migrations.AlterModelOptions(
            name='csvimport',
            options={'verbose_name': 'CSV import', 'verbose_name_plural': 'CSV imports'},
        ),
        migrations.AlterModelOptions(
            name='database',
            options={'verbose_name': 'database', 'verbose_name_plural': 'databases'},
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'entry', 'verbose_name_plural': 'entries'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'permissions': (('view', 'View'), ('change', 'View'), ('delete', 'View')), 'verbose_name': 'table', 'verbose_name_plural': 'tables'},
        ),
        migrations.AlterModelOptions(
            name='tablecolumn',
            options={'ordering': ['table', 'pk'], 'verbose_name': 'table column', 'verbose_name_plural': 'table columns'},
        ),
        migrations.AlterModelOptions(
            name='usercard',
            options={'ordering': ['order'], 'verbose_name': 'profile card', 'verbose_name_plural': 'profile cards'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'user profile', 'verbose_name_plural': 'user profiles'},
        ),
        migrations.AlterField(
            model_name='card',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='card',
            name='data_column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cards_column_fields', to='api.tablecolumn', verbose_name='data column'),
        ),
        migrations.AlterField(
            model_name='card',
            name='data_column_function',
            field=models.CharField(choices=[('Count', 'Count'), ('Sum', 'Sum'), ('Min', 'Min'), ('Max', 'Max'), ('Avg', 'Average'), ('StdDev', 'Standard Deviation')], default='Count', max_length=10, verbose_name='data column function'),
        ),
        migrations.AlterField(
            model_name='card',
            name='filters',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='filters'),
        ),
        migrations.AlterField(
            model_name='card',
            name='last_edit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last edit date'),
        ),
        migrations.AlterField(
            model_name='card',
            name='last_edit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_card_edits', to=settings.AUTH_USER_MODEL, verbose_name='last edit user'),
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='card',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='chart_type',
            field=models.CharField(choices=[('Line', 'Line'), ('Bar', 'Bar'), ('Pie', 'Pie'), ('Doughnut', 'Doughnut')], default='Line', max_length=20, verbose_name='chart type'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='filters',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='filters'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='last_edit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last edit date'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='last_edit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_chart_edits', to=settings.AUTH_USER_MODEL, verbose_name='last edit user'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='timeline_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='charts_timeline_fields', to='api.tablecolumn', verbose_name='timeline field'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='timeline_include_nulls',
            field=models.BooleanField(default=False, verbose_name='timeline include nulls'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='timeline_period',
            field=models.CharField(blank=True, choices=[('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')], default='minute', max_length=20, null=True, verbose_name='timeline period'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='x_axis_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='charts_x_axis_fields', to='api.tablecolumn', verbose_name='x axis field'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='x_axis_field_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='charts_x_axis_fields_group', to='api.tablecolumn', verbose_name='x axis field 2'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='y_axis_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='charts_y_axis_fields', to='api.tablecolumn', verbose_name='y axis field'),
        ),
        migrations.AlterField(
            model_name='chart',
            name='y_axis_function',
            field=models.CharField(choices=[('Count', 'Count'), ('Sum', 'Sum'), ('Min', 'Min'), ('Max', 'Max'), ('Avg', 'Average'), ('StdDev', 'Standard Deviation')], default='Count', max_length=10, verbose_name='y axis function'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='csv_import',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csv_field_mapping', to='api.csvimport', verbose_name='CSV import'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='display_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='display name'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='field_format',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='field format'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='field_type',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('int', 'int'), ('float', 'float'), ('date', 'date'), ('enum', 'enum')], default='text', max_length=20, null=True, verbose_name='field type'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='original_name',
            field=models.CharField(max_length=100, verbose_name='original name'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='required',
            field=models.BooleanField(default=False, verbose_name='required'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csv_field_mapping', to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='table_column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.tablecolumn', verbose_name='table column'),
        ),
        migrations.AlterField(
            model_name='csvfieldmap',
            name='unique',
            field=models.BooleanField(default=False, verbose_name='unique'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='delimiter',
            field=models.CharField(blank=True, default=';', max_length=2, null=True, verbose_name='delimiter'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='errors',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='errors'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='errors_count',
            field=models.IntegerField(default=0, verbose_name='errors count'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='file',
            field=models.FileField(upload_to='csvs/', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='import_count_created',
            field=models.IntegerField(default=0, verbose_name='import count created'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='import_count_skipped',
            field=models.IntegerField(default=0, verbose_name='import count skipped'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='import_count_updated',
            field=models.IntegerField(default=0, verbose_name='import count updated'),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csv_imports', to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='database',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='database',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='data',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='default_fields',
            field=models.ManyToManyField(blank=True, related_name='filter_default_field', to='api.TableColumn', verbose_name='default fields'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='filters',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='filters'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='join_tables',
            field=models.ManyToManyField(related_name='filter_join_table', to='api.FilterJoinTable', verbose_name='join tables'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='last_edit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last edit date'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='last_edit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_filter_edits', to=settings.AUTH_USER_MODEL, verbose_name='last edit user'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='primary_table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.filterjointable', verbose_name='primary table'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='filterjointable',
            name='fields',
            field=models.ManyToManyField(related_name='filter_join_table_fields', to='api.TableColumn', verbose_name='fields'),
        ),
        migrations.AlterField(
            model_name='filterjointable',
            name='join_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.tablecolumn', verbose_name='join field'),
        ),
        migrations.AlterField(
            model_name='filterjointable',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='table',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='table',
            name='database',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='api.database', verbose_name='database'),
        ),
        migrations.AlterField(
            model_name='table',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='table',
            name='default_fields',
            field=models.ManyToManyField(blank=True, related_name='default_field', to='api.TableColumn', verbose_name='default fields'),
        ),
        migrations.AlterField(
            model_name='table',
            name='filters',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='filters'),
        ),
        migrations.AlterField(
            model_name='table',
            name='last_edit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last edit date'),
        ),
        migrations.AlterField(
            model_name='table',
            name='last_edit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_table_edits', to=settings.AUTH_USER_MODEL, verbose_name='last edit user'),
        ),
        migrations.AlterField(
            model_name='table',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='table',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='table',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='choices',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None, verbose_name='choices'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='display_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='display name'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='field_type',
            field=models.CharField(choices=[('text', 'text'), ('int', 'int'), ('float', 'float'), ('date', 'date'), ('enum', 'enum')], max_length=20, verbose_name='field type'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='help_text',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='help text'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='required',
            field=models.BooleanField(default=False, verbose_name='required'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='api.table', verbose_name='table'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='unique',
            field=models.BooleanField(default=False, verbose_name='unique'),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.card', verbose_name='card'),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='order',
            field=models.IntegerField(default=1, help_text='What order to display this card within the profile dashboard.', verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_cards', to='api.userprofile', verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cards',
            field=models.ManyToManyField(blank=True, through='api.UserCard', to='api.Card', verbose_name='cards'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dashboard_charts',
            field=models.ManyToManyField(blank=True, to='api.Chart', verbose_name='dasbhoard charts'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dashboard_filters',
            field=models.ManyToManyField(blank=True, to='api.Filter', verbose_name='dashboard filters'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(blank=True, default='', help_text='Preferred language', max_length=10, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='token'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
