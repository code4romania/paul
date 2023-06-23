import os
import re
import uuid

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from djoser.signals import user_activated

from api import utils


@receiver(user_activated)
def user_activated_callback(sender, **kwargs):
    user = kwargs['user']
    Userprofile.objects.get_or_create(user=user)
    request = kwargs['request']
    user_group, created = Group.objects.get_or_create(name="user")
    user.groups.add(user_group)
    user.is_active = False
    user.save()

    admins = User.objects.filter(groups__name='admin')
    base_path = '{}://{}'.format(request.scheme, request.get_host())

    for admin in admins:
        utils.send_email(
            template="email/new_user.html",
            context={"admin": admin, "user": user, "base_path": base_path},
            subject=_("[PAUL] New user registered"),
            to=admin.email)


datatypes = (
    ("text", _("text")),
    ("int", _("int")),
    ("float", _("float")),
    ("date", _("date")),
    # ("bool", _("bool")),
    # ("object", _("object")),
    ("enum", _("enum")),
)

chart_functions = (
    ("Count", _("Count")),
    ("Sum", _("Sum")),
    ("Min", _("Min")),
    ("Max", _("Max")),
    ("Avg", _("Average")),
    ('StdDev', _("Standard Deviation")),
)

chart_types = (
    ("Line", _("Line")),
    ("Bar", _("Bar")),
    ("Pie", _("Pie")),
    ("Doughnut", _("Doughnut")),
)

chart_timeline_periods = (
    ("minute", _("Minute")),
    ("hour", _("Hour")),
    ("day", _("Day")),
    ("week", _("Week")),
    ("month", _("Month")),
    ("year", _("Year")),
)


class Userprofile(models.Model):
    """
    Description: An user profile for storing extra user account options
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile",
        verbose_name=_("user"))

    dashboard_filters = models.ManyToManyField("Filter", blank=True, verbose_name=_("dashboard filters"))
    dashboard_charts = models.ManyToManyField("Chart", blank=True, verbose_name=_("dasbhoard charts"))
    cards = models.ManyToManyField("Card", through='UserCard', blank=True, verbose_name=_("cards"))

    token = models.UUIDField(_("token"), default=uuid.uuid4)
    avatar = models.ImageField(_("avatar"), upload_to="avatars", null=True, blank=True)
    language = models.CharField(
        _("language"),
        max_length=10, default="", blank=True, null=False,
        help_text=_("Preferred language"))

    def full_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    @staticmethod
    def generate_username(email: str) -> str:
        """ 
        Generate an username from the provided email address by eliminating 
        blank spaces before & after it and by using lowercase letters
        """
        return email.lower().strip()


class UserCard(models.Model):
    """
    Description: Model Description
    """
    profile = models.ForeignKey(
        Userprofile, on_delete=models.CASCADE, related_name="dashboard_cards", verbose_name=_("profile"))
    card = models.ForeignKey("Card", on_delete=models.CASCADE, verbose_name=_("card"))
    order = models.IntegerField(
        _("order"),
        help_text=_("What order to display this card within the profile dashboard."),
        default=1
    )

    class Meta:
        verbose_name = _("profile card")
        verbose_name_plural = _("profile cards")
        ordering = ['order',]

    def __str__(self):
        return '{} - {} (o:{})'.format(
            self.profile,
            self.card,
            self.order)


class Database(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("database")
        verbose_name_plural = _("databases")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def active_tables(self):
        return self.tables.filter(active=True).order_by("id")

    def archived_tables(self):
        return self.tables.filter(active=False).order_by("id")

    def tables_count(self):
        return self.tables.count()


class Table(models.Model):
    """
    Description: Model Description
    """

    TYPE_REGULAR = ""
    TYPE_CONTACTS = "C"
    TYPES = (
        (TYPE_REGULAR, _("regular")),
        (TYPE_CONTACTS, _("contacts")),
    )

    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=50, null=True, blank=True)
    database = models.ForeignKey(
        "Database", on_delete=models.CASCADE, related_name="tables", verbose_name=_("database"))
    active = models.BooleanField(_("active"), default=False)

    date_created = models.DateTimeField(_("date created"), auto_now_add=timezone.now)
    default_fields = models.ManyToManyField(
        'TableColumn', blank=True, related_name='default_field',
        verbose_name=_("default fields"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("owner"))
    last_edit_date = models.DateTimeField(
        _("last edit date"), null=True, blank=True, db_index=True)
    last_edit_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="last_table_edits",
        verbose_name=_("last edit user")
    )
    table_type = models.CharField(
        _("type"), max_length=1, default=TYPE_REGULAR, null=False, blank=True, choices=TYPES)
    filters = models.JSONField(
        verbose_name=_("filters"),
        encoder=DjangoJSONEncoder, null=True, blank=True)

    class Meta:
        permissions = (
            ("update_content", _("Can update table content")),
        )
        unique_together = ["name", "database"]
        verbose_name = _("table")
        verbose_name_plural = _("tables")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = re.sub('_+', '_', self.name)
        self.slug = slugify(value, allow_unicode=True)
        self.last_edit_date = timezone.now()
        super().save(*args, **kwargs)

    def entries_count(self):
        return self.entries.count()


class TableColumn(models.Model):
    """
    Description: Model Description
    """

    table = models.ForeignKey(
        "Table", on_delete=models.CASCADE, related_name="fields",
        verbose_name=_("table"))
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    display_name = models.CharField(_("display name"), max_length=50, null=True, blank=True)
    slug = models.SlugField(_("slug"), max_length=50, null=True, blank=True)
    field_type = models.CharField(_("field type"), max_length=20, choices=datatypes)
    help_text = models.CharField(_("help text"), max_length=255, null=True, blank=True)
    choices = ArrayField(
        models.CharField(max_length=100), null=True, blank=True, verbose_name=_("choices"))
    required = models.BooleanField(_("required"), default=False)
    unique = models.BooleanField(_("unique"), default=False)

    class Meta:
        unique_together = ["table", "name"]
        ordering = ['table', 'pk']
        verbose_name = _("table column")
        verbose_name_plural = _("table columns")

    def __str__(self):
        return "[{}] {} ({})".format(self.table, self.name, self.field_type)

    def save(self, *args, **kwargs):
        value = re.sub('_+', '_', self.name)
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class CsvFieldMap(models.Model):
    """
    Description: Model Description
    """

    table = models.ForeignKey(
        "Table",
        on_delete=models.CASCADE,
        related_name="csv_field_mapping",
        null=True,
        blank=True,
        verbose_name=_("table"),
    )
    csv_import = models.ForeignKey(
        "CsvImport",
        on_delete=models.CASCADE,
        related_name="csv_field_mapping",
        null=True,
        blank=True,
        verbose_name=_("CSV import"),
    )
    original_name = models.CharField(_("original name"), max_length=100)
    display_name = models.CharField(_("display name"), max_length=100, null=True, blank=True)
    field_type = models.CharField(
        _("field type"),
        max_length=20, choices=datatypes, default=datatypes[0][0],
        null=True, blank=True)
    field_format = models.CharField(_("field format"), max_length=20, null=True, blank=True)
    required = models.BooleanField(_("required"), default=False)
    unique = models.BooleanField(_("unique"), default=False)
    table_column = models.ForeignKey(
        'TableColumn', null=True, blank=True, on_delete=models.CASCADE,
        verbose_name=_("table column"))

    class Meta:
        verbose_name = _("CSV field map")
        verbose_name_plural = _("CSV field maps")


class CsvImport(models.Model):
    """
    Description: Model Description
    """

    file = models.FileField(_("file"), upload_to="csvs/")
    delimiter = models.CharField(
        _("delimiter"),
        max_length=2, default=";", null=True, blank=True)
    table = models.ForeignKey(
        "Table",
        related_name="csv_imports",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("table"),
    )

    errors = models.JSONField(_("errors"), encoder=DjangoJSONEncoder, null=True, blank=True)
    errors_count = models.IntegerField(_("errors count"), default=0, blank=False, null=False)
    import_count_created = models.IntegerField(_("import count created"), default=0)
    import_count_updated = models.IntegerField(_("import count updated"), default=0)
    import_count_skipped = models.IntegerField(_("import count skipped"), default=0)
    date_created = models.DateTimeField(_("date created"), auto_now_add=timezone.now)

    class Meta:
        verbose_name = _("CSV import")
        verbose_name_plural = _("CSV imports")

    @staticmethod
    def delete_file(instance):
        if instance.file:
            if settings.USE_S3 or settings.USE_AZURE:
                instance.file.delete(save=False)
            elif os.path.isfile(instance.file.path):
                os.remove(instance.file.path)

    def save(self, *args, **kwargs):
        if self.pk and self.file:
            # Delete the previous file when the model instance 
            # is updated with a new file
            instance = CsvImport.objects.get(pk=self.pk)
            CsvImport.delete_file(instance)
        return super().save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=CsvImport)
def auto_delete_import_file(sender, instance, **kwargs):
    """Delete the uploaded file when the model instance is deleted"""
    CsvImport.delete_file(instance)


class Entry(models.Model):
    """
    Description: Model Description
    """

    table = models.ForeignKey(
        "Table", on_delete=models.CASCADE, related_name="entries",
        verbose_name=_("table"))
    data = models.JSONField(_("data"), encoder=DjangoJSONEncoder, null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=timezone.now)

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")

    def __str__(self):
        return self.table.name

    # def clean_fields(self, exclude=None):
    #     super().clean_fields(exclude=exclude)



class FilterJoinTable(models.Model):
    """
    Description: Model Description
    """

    # filter = models.ForeignKey(
    #     "Filter", on_delete=models.CASCADE, related_name="filter_join_tables"
    # )
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name=_("table"))
    fields = models.ManyToManyField(
        TableColumn, related_name="filter_join_table_fields", verbose_name=_("fields"))
    join_field = models.ForeignKey(
        TableColumn, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("join field"))

    class Meta:
        pass

    def __str__(self):
        return "{} [{}] ({})".format(
            self.table.name,
            self.join_field.name if self.join_field else None,
            ", ".join(self.fields.values_list("name", flat=True)),
        )


class TableLink(models.Model):
    entry = models.ForeignKey(
        Entry, null=False, on_delete=models.CASCADE,
        verbose_name=_("entry"))
    entry_field = models.ForeignKey(
        TableColumn, null=False, on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("entry field"))
    target_field = models.ForeignKey(
        TableColumn, null=False, on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("target field"))
    created_on = models.DateTimeField(
        auto_now_add=timezone.now, editable=False,
        verbose_name=_("created on"))

    class Meta:
        pass


class Filter(models.Model):
    """
    Description: Model Description
    """

    name = models.CharField(_("name"), max_length=50, unique=True)
    slug = models.SlugField(_("slug"), max_length=50, null=True, blank=True)
    primary_table = models.ForeignKey(
        FilterJoinTable, null=True, on_delete=models.CASCADE,
        verbose_name="primary table")
    join_tables = models.ManyToManyField(
        FilterJoinTable, related_name="filter_join_table", verbose_name=_("join tables"))
    filters = models.JSONField(
        _("filters"),
        encoder=DjangoJSONEncoder, null=True, blank=True)
    creation_date = models.DateTimeField(
        _("creation date"), auto_now_add=timezone.now, null=True, db_index=True)
    default_fields = models.ManyToManyField(
        TableColumn, related_name="filter_default_field", blank=True,
        verbose_name=_("default fields"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
        verbose_name=_("owner"))
    last_edit_date = models.DateTimeField(
        _("last edit date"), null=True, blank=True, db_index=True)
    last_edit_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="last_filter_edits",
        verbose_name=_("last edit user"),
    )

    class Meta:
        pass

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = re.sub('_+', '_', self.name)
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Chart(models.Model):
    """
    Description: Model for representing a table chart
    """

    name = models.CharField(_("name"), max_length=100, unique=True)
    chart_type = models.CharField(
        _("chart type"),
        max_length=20, default=chart_types[0][0], choices=chart_types)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name=_("table"))
    timeline_field = models.ForeignKey(
        TableColumn, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="charts_timeline_fields",
        verbose_name=_("timeline field"),
    )
    timeline_period = models.CharField(
        _("timeline period"),
        max_length=20, null=True, blank=True,
        choices=chart_timeline_periods, default=chart_timeline_periods[0][0])
    timeline_include_nulls = models.BooleanField(_("timeline include nulls"), default=False)
    x_axis_field = models.ForeignKey(
        TableColumn, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="charts_x_axis_fields",
        verbose_name=_("x axis field"),
    )
    x_axis_field_2 = models.ForeignKey(
        TableColumn, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="charts_x_axis_fields_group",
        verbose_name=_("x axis field 2"),
    )
    y_axis_field = models.ForeignKey(
        TableColumn, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="charts_y_axis_fields",
        verbose_name=_("y axis field"),
    )
    y_axis_function = models.CharField(
        _("y axis function"),
        max_length=10, default=chart_functions[0][0], choices=chart_functions)

    filters = models.JSONField(
        _("filters"),
        encoder=DjangoJSONEncoder, null=True, blank=True)

    creation_date = models.DateTimeField(
        _("creation date"), auto_now_add=timezone.now, null=True, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name=_("owner"))
    last_edit_date = models.DateTimeField(
        _("last edit date"), null=True, blank=True, db_index=True)
    last_edit_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="last_chart_edits",
        verbose_name=_("last edit user"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Card(models.Model):
    """
    Description: Model for representing a table chart
    """

    name = models.CharField(_("name"), max_length=100, unique=True)

    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name=_("table"),)
    data_column_function = models.CharField(
        _("data column function"),
        max_length=10, default=chart_functions[0][0], choices=chart_functions)

    data_column = models.ForeignKey(
        TableColumn, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="cards_column_fields",
        verbose_name=_("data column"),
    )

    filters = models.JSONField(
        _("filters"),
        encoder=DjangoJSONEncoder, null=True, blank=True)

    creation_date = models.DateTimeField(
        _("creation date"), auto_now_add=timezone.now, null=True, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name=_("owner"))
    last_edit_date = models.DateTimeField(
        _("last edit date"), null=True, blank=True, db_index=True)
    last_edit_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="last_card_edits",
        verbose_name=_("last edit user"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class PluginTaskResult(models.Model):
    """
    Description: Model Description
    """
    
    RUNNING = "In progress"
    FINISHED = "Finished"
    STATUS_CHOICES = (
        (RUNNING, _("In progress")),
        (FINISHED, _("Finished")),
    )

    name = models.CharField(_("name"), max_length=255, null=True, blank=True)
    status = models.CharField(
        _("status"), 
        max_length=11, 
        default=RUNNING, 
        choices=STATUS_CHOICES,
        db_index=True
    )

    date_start = models.DateTimeField(_("date start"), auto_now_add=timezone.now)
    date_end = models.DateTimeField(_("date end"), null=True, blank=True)
    duration = models.DurationField(_("duration"), null=True, blank=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_tasks",
        verbose_name=_("user")
    )
    success = models.BooleanField(_("success"), default=False)
    stats = models.JSONField(
        _("stats"),
        encoder=DjangoJSONEncoder, null=True, blank=True
    )

    class Meta:
        abstract = True
        ordering = ['-id']
