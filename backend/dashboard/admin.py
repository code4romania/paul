from unfold.sites import UnfoldAdminSite
from django.utils.translation import gettext_lazy as _


class PaulAdminSite(UnfoldAdminSite):
    index_title = _("Welcome to Paul")
    index_template = "dashboard/index.html"
    site_header = _("Paul")
    site_title = _("Paul")
    site_url = None

    def each_context(self, request):
        context = super().each_context(request)
        context.update(
            {
                "app_dashboard": True,
            }
        )
        return context


dashboard_site = PaulAdminSite(name="app")
