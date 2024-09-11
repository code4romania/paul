from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin.exceptions import NotRegistered
from unfold.admin import ModelAdmin

from dashboard.admin import dashboard_site
from .models import User


# Remove the default admins for User and Group
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except NotRegistered:
    pass


# Register new admins for User and Group
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# Custom dashboards:


class UserDashboard(ModelAdmin):
    list_display = ("view_full_name", "view_role", "date_joined", "last_login")
    readonly_fields = ("last_login", "date_joined")
    exclude = ("password",)

    def user_name(self):
        return "asdasd"

    @admin.display(empty_value="", description=_("Full Name"))
    def view_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(empty_value="", description=_("Role"))
    def view_role(self, obj):
        return ""

    def changelist_view(self, request, extra_context=None):
        extra_context = {"title": _("Manage users")}
        return super().changelist_view(request, extra_context=extra_context)


dashboard_site.register(User, UserDashboard)
