from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        site = Site.objects.last()
        site.domain = settings.FRONTEND_DOMAIN
        site.name = settings.FRONTEND_DOMAIN
        site.save()
        print(_("New frontend domain: {domain}").format(domain=settings.FRONTEND_DOMAIN))