from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PluginMailchimpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugin_mailchimp"
    verbose_name = _("Plugin: Mailchimp")
