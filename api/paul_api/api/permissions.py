from guardian.core import ObjectPermissionChecker
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from api.models import Table


class BaseModelPermissions(permissions.DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsAuthenticatedOrGetToken(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        token_str = request.GET.get("token")
        token = Token.objects.filter(key=token_str)
        if token.exists():
            return True

        if request.user.is_authenticated:
            return True

        return False


class NoPermission(permissions.BasePermission):
    """
    Deny everybody
    """
    def has_permission(self, request, view):
        return False


class TableEntryPermissions(IsAuthenticatedOrGetToken):
    """
    Permission checks for actions performed on table Entry objects
    based on the parent table permission levels

    The parent table id must be provided in the view's kwargs as table_pk.
    """

    def has_permission(self, request, view):
        table_pk = view.kwargs.get("table_pk", 0)
        try:
            table = Table.objects.get(pk=table_pk)
        except Table.DoesNotExist:
            return False

        checker = ObjectPermissionChecker(request.user)
        user_perms = checker.get_perms(table)
        
        READ_ACTIONS = ['list', 'retrieve']
        WRITE_ACTIONS = ['create', 'update', 'partial_update', 'destroy']

        if view.action in READ_ACTIONS and 'view_table' in user_perms:
            return True
        elif view.action in WRITE_ACTIONS and 'update_content' in user_perms:
            return True

        return False


class TableCustomActionPermissions(IsAuthenticatedOrGetToken):
    """
    Permission checks for custom actions performed on Tables

    The current table id must be provided in the view's kwargs as pk.
    """

    def has_permission(self, request, view):
        
        # Check if a valid token or session was provided
        if not super().has_permission(request, view):
            return False

        if request.user.is_authenticated:
            user = request.user
        else:
            try:
                user = Token.objects.get(key=request.GET.get("token")).user
            except Token.DoesNotExist:
                return False

        table_pk = view.kwargs.get("pk", 0)
        try:
            table = Table.objects.get(pk=table_pk)
        except Table.DoesNotExist:
            return False

        checker = ObjectPermissionChecker(user)
        user_perms = checker.get_perms(table)
        
        READ_ACTIONS = ['csv_export', 'xlsx_export']

        if view.action in READ_ACTIONS and 'view_table' in user_perms:
            return True

        return False
