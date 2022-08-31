from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.urls import reverse
from django.db.models import ImageField
from rest_framework.response import Response
from rest_framework import serializers

from api import models, utils
from pprint import pprint

from guardian.shortcuts import assign_perm, remove_perm
from guardian.core import ObjectPermissionChecker


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        userprofile = models.Userprofile.objects.create(user=new_user)
        user_group, _ = Group.objects.get_or_create(name="user")
        new_user.groups.add(user_group)
        return new_user


class UserUpdateSerializer(serializers.ModelSerializer):
    tables_permissions = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source="userprofile.avatar", allow_null=True, required=False)

    class Meta:
        model = User
        fields = [
            "email", "avatar", "first_name", "last_name", "tables_permissions"]

    def partial_update(self, request, *args, **kwargs):
        return Response(1)

    def update(self, instance, validated_data):
        if self.partial:
            tables_permissions = self.initial_data.get("tables_permissions")
            if tables_permissions:
                for table_permission in tables_permissions:
                    table = models.Table.objects.get(pk=table_permission["id"])
                    if table_permission["permissions"] == "Editare":
                        assign_perm("change_table", instance, table)
                        assign_perm("view_table", instance, table)
                        assign_perm("delete_table", instance, table)
                    elif table_permission["permissions"] == "Vizualizare":
                        assign_perm("view_table", instance, table)
                        remove_perm("change_table", instance, table)
                        remove_perm("delete_table", instance, table)
                    else:
                        remove_perm("view_table", instance, table)
                        remove_perm("change_table", instance, table)
                        remove_perm("delete_table", instance, table)
        else:
            if validated_data.get('userprofile'):
                userprofile_data = validated_data.pop("userprofile")
                profile = models.Userprofile.objects.get(user=instance)
                profile.avatar = userprofile_data['avatar']
                profile.save()
            User.objects.filter(pk=instance.pk).update(**validated_data)

        instance.refresh_from_db()

        return instance

    def get_tables_permissions(self, obj):
        tables = []

        checker = ObjectPermissionChecker(obj)

        for table in models.Table.objects.all():
            user_perms = checker.get_perms(table)

            if "change_table" in user_perms:
                table_perm = "Editare"
            elif "view_table" in user_perms:
                table_perm = "Vizualizare"
            else:
                table_perm = "Fără drepturi"
            tables.append({"name": table.name, "id": table.id, "permissions": table_perm})
        return tables


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    tables_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "url", "id", "username", "email", "is_active",
            "avatar", "first_name", "last_name",
            "tables_permissions"]

    def get_avatar(self, obj):
        try:
            request = self.context.get("request")
            avatar_url = obj.userprofile.avatar.url
            return request.build_absolute_uri(avatar_url)
        except:
            pass

    def get_tables_permissions(self, obj):
        tables = []

        checker = ObjectPermissionChecker(obj)

        for table in models.Table.objects.all():
            user_perms = checker.get_perms(table)
            pprint(user_perms)
            if "change_table" in user_perms:
                table_perm = "Editare"
            elif "view_table" in user_perms:
                table_perm = "Vizualizare"
            else:
                table_perm = "Fără drepturi"
            tables.append({"name": table.name, "id": table.id, "permissions": table_perm})
        return tables


class UserListDataSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "avatar",
            "first_name",
            "last_name",
        ]

    def get_avatar(self, obj):
        try:
            request = self.context.get("request")
            avatar_url = obj.userprofile.avatar.url
            return request.build_absolute_uri(avatar_url)
        except:
            pass


class UserListSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "is_active",
            "data"
        ]

    def get_data(self, obj):
        serializer = UserListDataSerializer(obj, context=self.context)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "email",
            "avatar",
            "first_name",
            "last_name",
        ]

    def get_avatar(self, obj):
        try:
            request = self.context.get("request")
            avatar_url = obj.userprofile.avatar.url
            return request.build_absolute_uri(avatar_url)
        except:
            pass


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "first_name", "last_name"]
