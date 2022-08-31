from django.utils import timezone
from django.urls import reverse

from rest_framework import serializers

from api.serializers.users import OwnerSerializer
from api import models
from api.serializers.tables import TableColumnSerializer


class FilterEntrySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.get("context", {}).get("fields")

        super(FilterEntrySerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            for field_name in fields:
                # MappedField = DATATYPE_SERIALIZERS[table_fields[field_name].field_type]
                try:
                    self.fields[field_name] = serializers.CharField()
                except:
                    pass


class FilterListDataSerializer(serializers.ModelSerializer):
    tables = serializers.SerializerMethodField()
    show_in_dashboard = serializers.SerializerMethodField()
    owner = OwnerSerializer()

    def get_show_in_dashboard(self, obj):
        userprofile = self.context["request"].user.userprofile
        return obj in userprofile.dashboard_filters.all()

    def get_tables(self, obj):
        if obj.primary_table:
            tables = [obj.primary_table.table.name] + list(obj.join_tables.values_list("table__name", flat=True))
            return tables
        return "-"

    class Meta:
        model = models.Filter
        fields = [
            "name",
            "creation_date",
            "tables",
            "owner",
            "show_in_dashboard",
        ]


class FilterListSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        serializer = FilterListDataSerializer(obj, context=self.context)
        return serializer.data

    class Meta:
        model = models.Filter
        fields = ["url", "id", "data"]


class FilterJoinTableListSerializer(serializers.ModelSerializer):
    table = serializers.SerializerMethodField()
    join_field = serializers.SerializerMethodField()
    fields = TableColumnSerializer(many=True)

    class Meta:
        model = models.FilterJoinTable
        fields = ["table", "join_field", "fields"]

    def get_table(self, obj):
        return obj.table.name

    def get_join_field(self, obj):
        return obj.join_field.name


class FilterDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    last_edit_user = OwnerSerializer()

    entries = serializers.SerializerMethodField()
    config = serializers.SerializerMethodField()
    fields = serializers.SerializerMethodField(method_name="get_filter_fields")
    default_fields = serializers.SerializerMethodField()

    class Meta:
        model = models.Filter
        fields = [
            "url",
            "id",
            "name",
            "entries",
            "owner",
            "last_edit_user",
            "last_edit_date",
            "config",
            "fields",
            "default_fields",
            "filters",
        ]

    def get_filter_fields(self, obj):
        fields = []
        primary_table = obj.primary_table

        for field in primary_table.fields.all():
            field_dict = {
                    "id": field.id,
                    "table_id": primary_table.id,
                    "name": "{}__{}".format(primary_table.table.slug, field.name),
                    "display_name": field.display_name,
                    "field_type": field.field_type,
                    "choices": field.choices,
                    "sortable": False
                }
            if not obj.join_tables.all():
                field_dict['sortable'] = True
            fields.append(field_dict)
        if obj.join_tables.all():
            secondary_table = obj.join_tables.all()[0]
            for field in secondary_table.fields.all():
                fields.append(
                    {
                        "id": field.id,
                        "table_id": secondary_table.id,
                        "name": "{}__{}".format(secondary_table.table.slug, field.name),
                        "display_name": field.display_name,
                        "field_type": field.field_type,
                        "choices": field.choices,
                        "sortable": True
                    }
                )
        return fields

    def get_default_fields(self, obj):
        primary_table = obj.primary_table
        all_fields = []
        if obj.default_fields.all():
            for field in obj.default_fields.all():
                all_fields.append('{}__{}'.format(field.table.slug, field.name))
        else:
            all_fields = [
                "{}__{}".format(primary_table.table.slug, x.name) for x in primary_table.fields.all().order_by("id")
            ]
            if obj.join_tables.all():
                secondary_table = obj.join_tables.all()[0]
                all_fields += [
                    "{}__{}".format(secondary_table.table.slug, x.name) for x in secondary_table.fields.all().order_by("id")
                ]
        return all_fields

    def get_config(self, obj):
        serializer = FilterCreateSerializer(obj, context=self.context)
        return serializer.data

    def get_entries(self, obj):
        return self.context["request"].build_absolute_uri(reverse("filter-entries", kwargs={"pk": obj.pk}))


class FilterJoinTableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilterJoinTable
        fields = ["table", "fields", "join_field"]


class FilterCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    last_edit_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    last_edit_date = serializers.HiddenField(default=timezone.now())
    primary_table = FilterJoinTableCreateSerializer()
    join_tables = FilterJoinTableCreateSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.Filter
        fields = ["id", "name", "owner", "last_edit_user", "last_edit_date", "primary_table", "join_tables", "filters", "default_fields"]

    def create(self, validated_data):
        primary_table = validated_data.pop("primary_table")
        join_tables = validated_data.pop("join_tables")

        new_filter = models.Filter.objects.create(**validated_data)

        fields = primary_table.pop("fields")
        primary_table = models.FilterJoinTable.objects.create(**primary_table)
        primary_table.fields.set(fields)

        new_filter.primary_table = primary_table
        new_filter.save()

        if join_tables:
            for join_table in join_tables:
                fields = join_table.pop("fields")
                join_table = models.FilterJoinTable.objects.create(**join_table)
                join_table.fields.set(fields)

                new_filter.join_tables.add(join_table)
        return new_filter

    def update(self, instance, validated_data):

        if self.partial:
            if validated_data.get('filters'):
                filters = validated_data.pop('filters')
                models.Filter.objects.filter(pk=instance.pk).update(**{'filters': filters})
            if validated_data.get('default_fields'):
                default_fields = validated_data.pop('default_fields')
                if default_fields:
                    instance.default_fields.set([])
                    for field in default_fields:
                        instance.default_fields.add(field)
            instance.refresh_from_db()
        else:
            instance.name = validated_data.get("name")
            instance.last_edit_user = self.context['request'].user

            instance.filters = validated_data.get("filters")
            primary_table_data = validated_data.pop("primary_table")
            join_tables = validated_data.pop("join_tables")

            primary_table = instance.primary_table
            primary_table.table = primary_table_data["table"]
            primary_table.join_field = primary_table_data["join_field"]
            primary_table.fields.set(primary_table_data["fields"])
            primary_table.save()

            instance.join_tables.set([])
            for table in instance.join_tables.all():
                table.delete()
            for join_table in join_tables:
                fields = join_table.pop("fields")
                join_table = models.FilterJoinTable.objects.create(**join_table)
                join_table.fields.set(fields)

                instance.join_tables.add(join_table)
            instance.default_fields.set([])
            instance.save()
        return instance
