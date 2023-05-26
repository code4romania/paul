from datetime import datetime

from dateutil.parser import isoparse
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from guardian.core import ObjectPermissionChecker
from rest_framework import serializers

from api.models import Entry


datatypes = {
    "int": "int",
    "float": "float",
    "text": "text",
    "date": "date",
    "bool": "bool",
    "enum": "enum",
}


DATATYPE_SERIALIZERS = {
    "text": serializers.CharField,
    "float": serializers.FloatField,
    "int": serializers.IntegerField,
    "date": serializers.DateField,
    "bool": serializers.BooleanField,
    "enum": serializers.CharField,
}


class EntryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = []

    def __init__(self, *args, **kwargs):
        fields = kwargs.get("context", {}).get("fields")
        table = kwargs.get("context", {}).get("table")

        if table:
            table_fields = {field.name: field for field in table.fields.all()}

        super(EntryDataSerializer, self).__init__(*args, **kwargs)

        entry = args[0]
        if fields is not None:
            for field_name in fields:
                MappedField = DATATYPE_SERIALIZERS[table_fields[field_name].field_type]

                if args[0].data and field_name in args[0].data.keys() and args[0].data[field_name] != '':
                    self.fields[field_name] = MappedField(source="data.{}".format(field_name), required=False)


class EntryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["url", "id", "table", "date_created", "data"]

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse(
                "table-entries-detail",
                kwargs={"pk": obj.pk, "table_pk": obj.table.pk},
            )
        )


class EntrySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = ["url", "id", "date_created", "data"]

    def validate(self, attrs):
        table = self.context.get("table")
        table_fields = {field.name: field for field in table.fields.all()}
        errors = {}

        unknown = set(self.initial_data) - set(self.fields) - set(table_fields.keys())

        if unknown:
            errors["non_field_errors"] = _("Unknown fields: {field_names}").format(field_names=", ".join(unknown))

        for field_name, field_value in self.initial_data.items():
            if field_name in table_fields.keys():
                field = table_fields[field_name]

                if field.field_type == "int":
                    try:
                        int(field_value)
                    except:
                        errors[field_name] = _("{}: Integer is not valid").format(field_name)
                elif field.field_type == "float":
                    try:
                        float(field_value)
                    except:
                        errors[field_name] = _("{}: Float is not valid").format(field_name)
                elif field.field_type == "date":
                    try:
                        # datetime.strptime(field_value, "%Y-%m-%dT%H:%M:%S%z")
                        isoparse(field_value)
                    except Exception as e:
                        print(e)
                        errors[field_name] = _("{}: Invalid date format").format(field_name)
                elif field.field_type == "enum":
                    if field_value not in field.choices:
                        errors[field_name] = _(
                            "{field_name}: {field_value} is not a valid choice ({valid_choices})"
                        ).format(
                            field_name=field_name,
                            field_value=field_value, 
                            valid_choices=",".join(field.choices)
                        )

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def get_data(self, obj):
        serializer = EntryDataSerializer(obj, context=self.context)
        return serializer.data

    def __init__(self, *args, **kwargs):
        fields = kwargs.get("context", {}).get("fields")
        table = kwargs.get("context", {}).get("table")

        super(EntrySerializer, self).__init__(*args, **kwargs)

        self.fields["data"].context.update({"table": table, "fields": fields})

    def _set_field_types_and_uniqueness(self, table, data, entry_pk=0):
        fields = {x.name: x for x in table.fields.all()}
        unique_fields = [x.name for x in table.fields.all() if x.unique==True]

        if unique_fields and settings.USE_COMPOUND_CONSTRAINT:
            data_query = {}
            for field in unique_fields:
                if data.get(field, None):
                    data_query[field] = data.get(field, None)
            if Entry.objects.filter(table=table, data__contains=data_query).exclude(pk=entry_pk).exists():
                if len(unique_fields) > 1:
                    msg = _(
                        "The {unique_field_names} fields must be unique together"
                    ).format(unique_field_names=', '.join(unique_fields))
                else:
                    msg = _(
                        "The {unique_field_name} field must be unique in table"
                    ).format(unique_field_name=unique_fields[0])
                raise serializers.ValidationError(msg)
        elif unique_fields:
            duplicates = []
            for field in unique_fields:
                if Entry.objects.exclude(pk=entry_pk).filter(table=table, data__contains={field: data.get(field, None)}).exists():
                    duplicates.append(field)
            if duplicates:
                if len(duplicates) > 1:
                    msg = _(
                        "The {unique_field_names} fields must be unique in table"
                    ).format(unique_field_names=', '.join(duplicates))
                else:
                    msg = _(
                        "The {unique_field_name} field must be unique in table"
                    ).format(unique_field_name=duplicates[0])
                raise serializers.ValidationError(msg)                

        for field, field_obj in fields.items():
            value = data.get(field, None)
            if field_obj.required:
                if not value or value == "":
                    raise serializers.ValidationError(
                        _("The {field_name} field is required").format(field_name=field)
                    )
            if field_obj.field_type == "enum":
                if value and value not in field_obj.choices:
                    raise serializers.ValidationError(
                        _(
                            "The {field_name} field value must be one of: {field_choices}"
                        ).format(field_names=field, field_choices=", ".join(field_obj.choices))
                    )
            elif value and field_obj.field_type == "float":
                data[field] = float(data[field])
            elif value and field_obj.field_type == "int":
                data[field] = int(data[field])

        return data

    def create(self, validated_data):
        table = self.context["table"]
        validated_data["data"] = self.initial_data
        validated_data["table"] = table
        data = self._set_field_types_and_uniqueness(table, validated_data["data"])        
        instance = Entry.objects.create(table=table, data=data)
        instance.clean_fields()
        instance.save()
        instance.table.last_edit_user = self.context["request"].user
        instance.table.last_edit_date = timezone.now()
        instance.table.save()
        return instance

    def update(self, instance, validated_data, *args, **kwargs):
        table = instance.table
        data = self._set_field_types_and_uniqueness(table, self.initial_data, instance.pk)
        instance.data = data
        instance.save()
        instance.table.last_edit_user = self.context["request"].user
        instance.table.last_edit_date = timezone.now()
        instance.table.save()
        return instance

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse(
                "table-entries-detail",
                kwargs={"pk": obj.pk, "table_pk": obj.table.pk},
            )
        )
