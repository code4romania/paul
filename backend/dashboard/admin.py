from unfold.sites import UnfoldAdminSite
from django.utils.translation import gettext_lazy as _


class PaulAdminSite(UnfoldAdminSite):
    index_title = _("Welcome to Paul")
    index_template = "account_index.html"
    site_header = _("Paul")
    site_title = _("Paul")
    site_url = None


dashboard_site = PaulAdminSite(name="app")
