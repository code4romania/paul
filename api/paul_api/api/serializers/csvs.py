from rest_framework import serializers
from api import models


class CsvImportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CsvImport
        fields = ["url", "table", "id",
                  "file", "errors_count", "import_count_created", "import_count_updated"]


class CsvFieldMapSerializer(serializers.ModelSerializer):
    table_field = serializers.SerializerMethodField()

    class Meta:
        model = models.CsvFieldMap
        fields = ["original_name", "display_name", "field_type", "field_format", "table_field", "required", "unique"]

    def get_table_field(self, obj):
        if obj.table_column:
            return obj.table_column.pk
        return None


class CsvImportSerializer(serializers.ModelSerializer):
    csv_field_mapping = CsvFieldMapSerializer(many=True)
    filename = serializers.SerializerMethodField()

    class Meta:
        model = models.CsvImport
        fields = [
            "url",
            "table",
            "id",
            "file",
            "filename",
            "delimiter",
            "errors_count",
            "import_count_created",
            "import_count_updated",
            "errors",
            "csv_field_mapping",
        ]

    def get_filename(self, obj):
        return obj.file.name.split('/')[-1]