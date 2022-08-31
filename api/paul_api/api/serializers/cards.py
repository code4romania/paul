from django.utils import timezone
from django.urls import reverse

from rest_framework import serializers

from api.serializers.users import OwnerSerializer
from api import models


class ListDataSerializer(serializers.ModelSerializer):
    table = serializers.CharField(source="table.name")
    show_in_dashboard = serializers.SerializerMethodField()
    owner = OwnerSerializer()

    def get_show_in_dashboard(self, obj):
        userprofile = self.context["request"].user.userprofile
        return obj in userprofile.cards.all()

    class Meta:
        model = models.Card
        fields = [
            "name",
            "creation_date",
            "table",
            "owner",
            "show_in_dashboard",
            "filters"
        ]


class ListSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        serializer = ListDataSerializer(obj, context=self.context)
        return serializer.data

    class Meta:
        model = models.Card
        fields = ["url", "id", "data"]


class DetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    last_edit_user = OwnerSerializer()

    data = serializers.SerializerMethodField()
    config = serializers.SerializerMethodField()

    class Meta:
        model = models.Card
        fields = [
            "url",
            "id",
            "name",
            "data",
            "owner",
            "last_edit_user",
            "last_edit_date",
            "config",
            "filters",
        ]

    def get_config(self, obj):
        serializer = CreateSerializer(obj, context=self.context)
        return serializer.data

    def get_data(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse("card-data", kwargs={"pk": obj.pk}))


class CreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    last_edit_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    last_edit_date = serializers.HiddenField(
        default=timezone.now())

    class Meta:
        model = models.Card
        fields = [
            "id", "name", "owner", "last_edit_user", "last_edit_date",
            "table", "data_column_function", "data_column", "filters",
        ]

    # def create(self, validated_data):
    #     new_filter = models.Card.objects.create(**validated_data)

    #     return new_filter

    def update(self, instance, validated_data):
        if self.partial:
            models.Card.objects.filter(pk=instance.pk).update(**validated_data)
        else:
            validated_data.pop('filters')
            models.Card.objects.filter(pk=instance.pk).update(**validated_data)
        instance.refresh_from_db()
        return instance
