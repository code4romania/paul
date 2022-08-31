from rest_framework import serializers
from api import models
from django.urls import reverse
from datetime import datetime
from dateutil.parser import isoparse

from pprint import pprint

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
        model = models.Entry
        fields = []

    def __init__(self, *args, **kwargs):
        fields = kwargs.get("context", {}).get("fields")
        table = kwargs.get("context", {}).get("table")

        if table:
            table_fields = {field.name: field for field in table.fields.all()}

        super(EntryDataSerializer, self).__init__(*args, **kwargs)

        entry = args[0]
        # print(kwargs)
        if fields is not None:
            for field_name in fields:
                MappedField = DATATYPE_SERIALIZERS[table_fields[field_name].field_type]

                if args[0].data and field_name in args[0].data.keys() and args[0].data[field_name] != '':
                    self.fields[field_name] = MappedField(source="data.{}".format(field_name), required=False)


class EntrySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = ["url", "id", "date_created", "data"]

    def validate(self, attrs):
        table = self.context.get("table")
        table_fields = {field.name: field for field in table.fields.all()}
        errors = {}

        unknown = set(self.initial_data) - set(self.fields) - set(table_fields.keys())

        if unknown:
            errors["non_field_errors"] = "Unknown field(s): {}".format(", ".join(unknown))

        for field_name, field_value in self.initial_data.items():
            if field_name in table_fields.keys():
                field = table_fields[field_name]

                if field.field_type == "int":
                    try:
                        int(field_value)
                    except:
                        errors[field_name] = "Integer is not valid"
                elif field.field_type == "float":
                    try:
                        float(field_value)
                    except:
                        errors[field_name] = "Float is not valid"
                elif field.field_type == "date":
                    try:
                        # datetime.strptime(field_value, "%Y-%m-%dT%H:%M:%S%z")
                        isoparse(field_value)
                    except Exception as e:
                        print(e)
                        errors[field_name] = "Invalid date format"
                elif field.field_type == "enum":
                    if field_value not in field.choices:
                        errors[field_name] = "{} is not a valid choice({})".format(
                            field_value, ",".join(field.choices))

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

    

    def create(self, validated_data):
        table = self.context["table"]
        validated_data["data"] = self.initial_data
        validated_data["table"] = table

        fields = {x.name: x for x in table.fields.all()}
        unique_fields = [x.name for x in table.fields.all() if x.unique==True]
        if unique_fields:
            data_query = {}
            for field in unique_fields:
                if validated_data['data'].get(field, None):
                    data_query[field] = validated_data['data'].get(field, None)
            if models.Entry.objects.filter(data__contains=data_query).exists():
                if len(unique_fields) > 1:
                    msg = f"Câmpurile {', '.join(unique_fields)} trebuie sa fie unice împreuna"
                else:
                    msg = f"Câmpul {unique_fields[0]} trebuie sa fie unic în tabel"

                raise serializers.ValidationError(msg)
        for field, field_obj in fields.items():
            value = validated_data['data'].get(field, None)
            if field_obj.required:
                if not value or value == "":
                    
                    raise serializers.ValidationError("Câmpul {} este obligatoriu".format(field))
            if field_obj.field_type == "enum":
                if value and value not in field_obj.choices:
                    raise ValidationError(
                        "Valorea câmpului {} trebuie sa fie una din : {}".format(
                            field, ", ".join(field_obj.choices))
                    )
            elif value and field_obj.field_type == "float":
                validated_data['data'][field] = float(validated_data['data'][field])
            elif value and field_obj.field_type == "int":
                validated_data['data'][field] = int(validated_data['data'][field])


        
        instance = models.Entry.objects.create(**validated_data)
        instance.clean_fields()
        instance.save()
        instance.table.last_edit_user = self.context["request"].user
        instance.table.last_edit_date = datetime.now()
        instance.table.save()
        return instance

    def update(self, instance, validated_data, *args, **kwargs):
        table = instance.table

        fields = {x.name: x for x in table.fields.all()}
        unique_fields = [x.name for x in table.fields.all() if x.unique==True]
        if unique_fields:
            data_query = {}
            for field in unique_fields:
                if self.initial_data.get(field, None):
                    data_query[field] = self.initial_data.get(field, None)
            if models.Entry.objects.filter(data__contains=data_query).exclude(pk=instance.pk).exists():
                if len(unique_fields) > 1:
                    msg = f"Câmpurile {', '.join(unique_fields)} trebuie sa fie unice împreuna"
                else:
                    msg = f"Câmpul {unique_fields[0]} trebuie sa fie unic în tabel"

                raise serializers.ValidationError(msg)
        for field, field_obj in fields.items():
            value = self.initial_data.get(field, None)
            if field_obj.required:
                if not value or value == "":
                    
                    raise serializers.ValidationError("Câmpul {} este obligatoriu".format(field))
            if field_obj.field_type == "enum":
                if value and value not in field_obj.choices:
                    raise ValidationError(
                        "Valorea câmpului {} trebuie sa fie una din : {}".format(
                            field, ", ".join(field_obj.choices))
                    )
            elif value and field_obj.field_type == "float":
                self.initial_data[field] = float(self.initial_data[field])
            elif value and field_obj.field_type == "int":
                self.initial_data[field] = int(self.initial_data[field])

        instance.data = self.initial_data
        instance.table.last_edit_user = self.context["request"].user
        instance.table.last_edit_date = datetime.now()
        instance.table.save()
        instance.save()
        return instance

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse(
                "table-entries-detail",
                kwargs={"pk": obj.pk, "table_pk": obj.table.pk},
            )
        )
