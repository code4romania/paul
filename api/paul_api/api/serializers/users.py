from django.contrib.auth.models import Group, User
from django.db import IntegrityError, transaction
from django.utils.translation import ugettext_lazy as _
from djoser.conf import settings as djsettings
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework import serializers
from rest_framework.response import Response

from api import models


def generate_username(email: str) -> str:
    """ 
    Generate an username from the provided email address by eliminating 
    blank spaces before & after it and by using lowercase letters
    """
    return email.lower().strip()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]

    def create(self, validated_data):
        # Create a new user with the same username as the email
        username = generate_username(validated_data["email"])
        try:
            new_user = User.objects.create(
                email=validated_data["email"], 
                username=username)
        except IntegrityError:
            raise serializers.ValidationError(
                _("An account with the %s username already exists" % username))

        models.Userprofile.objects.create(user=new_user)
        user_group, created = Group.objects.get_or_create(name="user")
        new_user.groups.add(user_group)
        
        # Send the initial password reset
        request = self.context.get("request")
        djsettings.EMAIL.password_reset(request, {"user": new_user, "initial": True}).send([new_email])

        return new_user


class UserUpdateSerializer(serializers.ModelSerializer):
    tables_permissions = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source="userprofile.avatar", allow_null=True, required=False)
    language = serializers.CharField(source="userprofile.language")

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
            username = generate_username(validated_data["email"])
            duplicate_username = False
            with transaction.atomic():
                # Update the username to match the email address
                if User.objects.filter(
                    username__iexact=username).exclude(pk=instance.pk).count():
                        duplicate_username = True
                else:
                    validated_data['username'] = username

                if not duplicate_username:
                    if validated_data.get('userprofile'):
                        userprofile_data = validated_data.pop("userprofile")
                        profile = models.Userprofile.objects.get(user=instance)
                        profile.avatar = userprofile_data['avatar']
                        profile.language = userprofile_data['language']
                        profile.save()
                    User.objects.filter(pk=instance.pk).update(**validated_data)
            
            if duplicate_username:
                raise serializers.ValidationError(
                    _("An account with the %s username already exists" % username))

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
    language = serializers.CharField(source="userprofile.language")

    class Meta:
        model = User
        fields = [
            "url", "id", "username", "email", "is_active",
            "language", "avatar", "first_name", "last_name",
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
    language = serializers.CharField(source="userprofile.language")

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
    language = serializers.CharField(source="userprofile.language")

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
