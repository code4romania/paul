
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import Group, User
from django.conf import settings
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework import serializers
from rest_framework.response import Response

from api import models


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]

    def create(self, validated_data):
        # Create a new user with the same username as the email
        new_email = validated_data["email"].lower().strip()
        new_user = User.objects.create(
            email=new_email, 
            username=new_email)
        models.Userprofile.objects.create(user=new_user)
        user_group, _ = Group.objects.get_or_create(name="user")
        new_user.groups.add(user_group)
        
        # Send the initial password reset
        form = PasswordResetForm({'email': new_email})
        request = self.context.get("request")
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=settings.NO_REPLY_EMAIL,
                email_template_name='mail/new_user_password.html')

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
            if validated_data.get('userprofile'):
                userprofile_data = validated_data.pop("userprofile")
                profile = models.Userprofile.objects.get(user=instance)
                profile.avatar = userprofile_data['avatar']
                profile.language = userprofile_data['language']
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
