from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        site = Site.objects.last()
        site.domain = settings.FRONTEND_DOMAIN
        site.name = settings.FRONTEND_DOMAIN
        site.save()
        print(f"New frontend domain: {settings.FRONTEND_DOMAIN}")