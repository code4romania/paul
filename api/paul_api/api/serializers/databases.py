from rest_framework import serializers
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import get_objects_for_user
from api.serializers.users import OwnerSerializer
from api import models


class DatabaseTableListDataSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()
    # last_edit_user = serializers.ReadOnlyField(source='last_edit_user.userprofile.full_name')
    last_edit_user = OwnerSerializer()

    def get_entries(self, obj):
        return obj.entries.count()

    class Meta:
        model = models.Table
        fields = [
            "name",
            "entries",
            "last_edit_date",
            "last_edit_user",
        ]


class DatabaseTableListSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    data = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()

    def get_data(self, obj):
        serializer = DatabaseTableListDataSerializer(obj, context=self.context)
        return serializer.data

    def get_user_permissions(self, obj):
        user = self.context["request"].user
        checker = ObjectPermissionChecker(user)

        user_perms = checker.get_perms(obj)
        return user_perms

    class Meta:
        model = models.Table
        fields = ["url", "id", "active", "owner", "data", "user_permissions"]


class DatabaseSerializer(serializers.HyperlinkedModelSerializer):
    active_tables = serializers.SerializerMethodField()
    archived_tables = serializers.SerializerMethodField()

    class Meta:
        model = models.Database
        fields = [
            "url",
            "id",
            "name",
            "active_tables",
            "archived_tables",
        ]

    def get_active_tables(self, obj):
        user = self.context['request'].user
        checker = ObjectPermissionChecker(user)

        tables = obj.active_tables()
        queryset = []
        for table in tables:
            user_perms = checker.get_perms(table)
            if 'view_table' in user_perms:
                queryset.append(table)
        serializer = DatabaseTableListSerializer(queryset, many=True, read_only=True, context=self.context)
        return serializer.data

    def get_archived_tables(self, obj):
        user = self.context['request'].user
        checker = ObjectPermissionChecker(user)

        tables = obj.archived_tables()
        queryset = []
        for table in tables:
            user_perms = checker.get_perms(table)
            if 'view_table' in user_perms:
                queryset.append(table)
        serializer = DatabaseTableListSerializer(queryset, many=True, read_only=True, context=self.context)
        return serializer.data