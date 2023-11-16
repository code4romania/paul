from rest_framework import serializers

from api.models import TableLink


class TableLinkSerializer(serializers.ModelSerializer):
    # TODO: Check user permission for source & target table read
    class Meta:
        model = TableLink
        fields = ["entry", "entry_field", "target_field"]
