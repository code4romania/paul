from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext as _


class User(AbstractUser):
    # We ignore the `username`` field because we will use the `email` for the authentication
    username = models.CharField(
        blank=True,
        editable=True,
        help_text=_("We do not use this field"),
        max_length=150,
        null=True,
        unique=True,
        validators=[],
        verbose_name=_("username"),
    )
    email = models.EmailField(verbose_name=_("email address"), blank=False, null=False, unique=True)
    is_ngohub_user = models.BooleanField(default=False, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        constraints = [
            models.UniqueConstraint(Lower("email"), name="email_unique"),
        ]
