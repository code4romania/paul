from django.contrib.auth.models import Group, User
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings as djsettings
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework import serializers
from rest_framework.response import Response

from api.models import Table, Userprofile


class AvatarMixin:
    def get_avatar(self, obj):
        try:
            request = self.context.get("request")
            avatar_url = obj.userprofile.avatar.url
            return request.build_absolute_uri(avatar_url)
        except:
            pass


class TablesPermissionsMixin:
    def get_tables_permissions(self, obj):
        tables_permissions = []
        checker = ObjectPermissionChecker(obj)

        for table in Table.objects.all():
            user_perms = checker.get_perms(table)
            if "change_table" in user_perms:
                table_perm_text = _("Edit")
                table_perm = "change_table"
            elif "update_content" in user_perms:
                table_perm_text = _("Update content")
                table_perm = "update_content"
            elif "view_table" in user_perms:
                table_perm_text = _("View")
                table_perm = "view_table"
            else:
                table_perm_text = _("No permissions")
                table_perm = ""
            tables_permissions.append({
                "name": table.name, 
                "id": table.id, 
                "permissions": table_perm,
                "permissions_text": table_perm_text,
            })
        return tables_permissions


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]

    def create(self, validated_data):
        # Create a new user with the same username as the email
        username = Userprofile.generate_username(validated_data["email"])
        try:
            new_user = User.objects.create(
                email=validated_data["email"], 
                username=username)
        except IntegrityError:
            raise serializers.ValidationError(
                _("An account with the {username} username already exists").format(username=username))

        Userprofile.objects.create(user=new_user)
        user_group, created = Group.objects.get_or_create(name="user")
        new_user.groups.add(user_group)
        
        # Send the initial password reset
        request = self.context.get("request")
        djsettings.EMAIL.password_reset(
            request, {"user": new_user, "initial": True}).send([validated_data["email"]])

        return new_user


class UserUpdateSerializer(TablesPermissionsMixin, serializers.ModelSerializer):
    tables_permissions = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source="userprofile.avatar", allow_null=True, required=False)
    language = serializers.CharField(source="userprofile.language", required=False)

    class Meta:
        model = User
        fields = [
            "email", "language", "avatar", "first_name", "last_name", "tables_permissions"]

    def partial_update(self, request, *args, **kwargs):
        return Response(1)

    def update(self, instance, validated_data):
        if self.partial:
            tables_permissions = self.initial_data.get("tables_permissions")
            if tables_permissions:
                for table_permission in tables_permissions:
                    table = Table.objects.get(pk=table_permission["id"])
                    if table_permission["permissions"] == "change_table":
                        assign_perm("change_table", instance, table)
                        assign_perm("delete_table", instance, table)
                        assign_perm("update_content", instance, table)
                        assign_perm("view_table", instance, table)
                    elif table_permission["permissions"] == "update_content":
                        remove_perm("change_table", instance, table)
                        remove_perm("delete_table", instance, table)
                        assign_perm("update_content", instance, table)
                        assign_perm("view_table", instance, table)
                    elif table_permission["permissions"] == "view_table":
                        remove_perm("change_table", instance, table)
                        remove_perm("delete_table", instance, table)
                        remove_perm("update_content", instance, table)
                        assign_perm("view_table", instance, table)
                    else:
                        remove_perm("change_table", instance, table)
                        remove_perm("delete_table", instance, table)
                        remove_perm("update_content", instance, table)
                        remove_perm("view_table", instance, table)
        else:
            username = Userprofile.generate_username(validated_data["email"])
            duplicate_username = False
            with transaction.atomic():
                # Update the username to match the email address
                if User.objects.filter(
                    username__iexact=username).exclude(pk=instance.pk).count():
                        duplicate_username = True
                else:
                    validated_data["username"] = username

                if not duplicate_username:
                    if validated_data.get("userprofile"):
                        userprofile_data = validated_data.pop("userprofile")
                        profile = Userprofile.objects.get(user=instance)
                        profile.avatar = userprofile_data.get("avatar")
                        profile.language = userprofile_data.get("language", "")
                        profile.save()
                    User.objects.filter(pk=instance.pk).update(**validated_data)
            
            if duplicate_username:
                raise serializers.ValidationError(
                    _("An account with the {username} username already exists").format(username=username))

        instance.refresh_from_db()
        return instance


class UserDetailSerializer(AvatarMixin, TablesPermissionsMixin, serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    tables_permissions = serializers.SerializerMethodField()
    language = serializers.CharField(source="userprofile.language", required=False)

    class Meta:
        model = User
        fields = [
            "url", "id", "username", "email", "is_active",
            "language", "avatar", "first_name", "last_name",
            "tables_permissions"]


class UserListDataSerializer(AvatarMixin, serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    language = serializers.CharField(source="userprofile.language", required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "language",
            "avatar",
            "first_name",
            "last_name",
        ]


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


class UserSerializer(AvatarMixin, serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    language = serializers.CharField(source="userprofile.language", required=False)

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "email",
            "language",
            "avatar",
            "first_name",
            "last_name",
        ]


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "first_name", "last_name"]
