from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import serializers

from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin

from api.serializers.users import OwnerSerializer, UserSerializer
from api import models, utils
from pprint import pprint


class TableColumnSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # choices = serializers.SerializerMethodField()

    class Meta:
        model = models.TableColumn
        fields = [
            "id",
            "name",
            "display_name",
            "field_type",
            "help_text",
            "required",
            "unique",
            "choices",
        ]

    # def get_choices(self, obj):
    #     if type(obj.choices) == list:
    #         return sorted([x for x in obj.choices if x])
    #     return []


class TableDatabaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Database
        fields = ["url", "id", "name", "slug"]


class TableCreateSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    database = serializers.PrimaryKeyRelatedField(queryset=models.Database.objects.all())
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    last_edit_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    last_edit_date = serializers.HiddenField(default=timezone.now())
    active = serializers.BooleanField(default=True)
    fields = TableColumnSerializer(many=True, required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.Table
        fields = [
            "id",
            "database",
            "name",
            "owner",
            "fields",
            "default_fields",
            "filters",
            "last_edit_user",
            "last_edit_date",
            "active",
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'database'),
                message="Această denumire de tabel este folosită deja."
            )
        ]

    def validate(self, data):
        if "id" in data.keys():
            table = models.Table.objects.get(pk=data["id"])
            if table.entries.exists():
                if "fields" in data.keys():
                    for field in data.get("fields"):
                        if "id" in field.keys():
                            field_obj = models.TableColumn.objects.get(pk=field["id"])
                            if field_obj.field_type != field["field_type"]:
                                raise serializers.ValidationError(
                                    {
                                        "fields-{}".format(
                                            field["id"]
                                        ): "Changing field type is not permited on a table with entries"
                                    }
                                )
        return data

    def create(self, validated_data):
        temp_fields = []
        if "fields" in validated_data.keys():
            temp_fields = validated_data.pop("fields")

        new_table = models.Table.objects.create(**validated_data)
        for i in temp_fields:
            if "display_name" not in i.keys():
                i["display_name"] = i["name"]
                i["name"] = utils.snake_case(i["name"])
            if "name" not in i.keys():
                i["name"] = utils.snake_case(i["display_name"])

            models.TableColumn.objects.create(table=new_table, **i)

        return new_table

    def update(self, instance, validated_data):
        if self.partial:
            if validated_data.get('filters'):
                filters = validated_data.pop('filters')
                if filters:
                    models.Table.objects.filter(pk=instance.pk).update(**{'filters': filters})
            if validated_data.get('default_fields'):
                default_fields = validated_data.pop('default_fields')
                if default_fields:
                    for field in default_fields:
                        instance.default_fields.add(field)
            instance.refresh_from_db()
        else:
            instance.name = validated_data.get("name")
            instance.active = validated_data.get("active")
            instance.database = validated_data.get("database")
            instance.last_edit_user = self.context["request"].user
            if "fields" in validated_data.keys():
                # Check to see if we need to delete any field
                old_fields_ids = set(instance.fields.values_list("id", flat=True))
                new_fields_ids = set([x.get("id") for x in validated_data.get("fields")])
                for id_to_remove in old_fields_ids - new_fields_ids:
                    field = models.TableColumn.objects.get(pk=id_to_remove)
                    field_name = field.name
                    field.delete()
                    for entry in instance.entries.all():
                        del entry.data[field_name]
                        entry.save()
                # Create or update fields
                for field in validated_data.pop("fields"):
                    if "id" in field.keys():
                        field_obj = models.TableColumn.objects.get(pk=field["id"])
                        old_name = field_obj.name
                        new_name = field["name"]
                        if old_name != new_name:

                            for entry in instance.entries.all():
                                entry.data[new_name] = entry.data[old_name]
                                del entry.data[old_name]
                                entry.save()
                        field_obj.__dict__.update(field)
                        field_obj.save()
                    else:

                        field["table"] = instance
                        field["name"] = utils.snake_case(field["display_name"])
                        models.TableColumn.objects.create(**field)

            instance.save()
        return instance

    def get_permissions_map(self, created):
        current_user = self.context["request"].user
        admins = Group.objects.get(name="admin")

        return {
            "view_table": [current_user, admins],
            "change_table": [current_user, admins],
            "delete_table": [current_user, admins],
        }


class TableSerializer(serializers.ModelSerializer):
    database = TableDatabaseSerializer()
    owner = OwnerSerializer(read_only=True)
    last_edit_user = UserSerializer(read_only=True)
    fields = TableColumnSerializer(many=True)
    entries = serializers.SerializerMethodField()
    default_fields = serializers.SerializerMethodField()

    class Meta:
        model = models.Table
        fields = [
            "url",
            "id",
            "name",
            "entries",
            "entries_count",
            "database",
            "slug",
            "owner",
            "last_edit_user",
            "last_edit_date",
            "date_created",
            "active",
            "default_fields",
            "fields",
            "filters"
        ]

    def get_default_fields(self, obj):
        if obj.default_fields.all():
            return [x for x in obj.default_fields.values_list("name", flat=True).order_by("id")]
        return [x for x in obj.fields.values_list("name", flat=True).order_by("id")]

    def get_entries(self, obj):
        return self.context["request"].build_absolute_uri(reverse("table-entries-list", kwargs={"table_pk": obj.pk}))



