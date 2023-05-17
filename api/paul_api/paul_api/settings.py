"""
Django settings for paul_api project.

Generated by 'django-admin startproject' using Django 3.1rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

root = environ.Path(__file__) - 3

env = environ.Env(
    # set casting, default value
    # aws settings
    USE_S3=(bool, False),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    AWS_SUBDOMAIN=(str, "s3.amazonaws.com"),
    AWS_S3_REGION_NAME=(str, ""),
    AWS_DEFAULT_ACL=(str, "public-read"),
    # azure settings
    USE_AZURE=(bool, False),
    AZURE_ACCOUNT_NAME=(str, ""),
    AZURE_ACCOUNT_KEY=(str, ""),
    AZURE_CONTAINER=(str, "data"),
    # django settings
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_TLS=(str, ""),
    IS_CONTAINERIZED=(bool, False),
    LANGUAGE_CODE=(str, "ro"),
    TIME_ZONE=(str, "Europe/Bucharest"),
    SECRET_KEY=(str, "secret"),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, ""),
    SENTRY_TRACES_SAMPLE_RATE=(float, 0.0),
    BACKGROUND_WORKERS=(int, 3),
    ADMIN_SITE_TITLE=(str, "PAUL Admin"),
    ADMIN_SITE_HEADER=(str, "PAUL"),
    MAILCHIMP_KEY=(str, ""),
)
environ.Env.read_env(f"{root}/.env")  # reading .env file

# some settings will be different if it's not running in a container (i.e. locally, on a Mac)
IS_CONTAINERIZED = env.bool("IS_CONTAINERIZED")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

CORS_ORIGIN_ALLOW_ALL = True
X_FRAME_OPTIONS = "SAMEORIGIN"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

USE_S3 = (
    env.bool("USE_S3")
    and env("AWS_ACCESS_KEY_ID")
    and env("AWS_SECRET_ACCESS_KEY")
    and env("AWS_STORAGE_BUCKET_NAME")
)
USE_AZURE = (
    env.bool("USE_AZURE") and env("AZURE_ACCOUNT_NAME") and env("AZURE_ACCOUNT_KEY")
)


TASK_DEFAULT_USERNAME = "paul-sync"

MAILCHIMP_KEY = env("MAILCHIMP_KEY")
PLUGIN_MAILCHIMP_ENABLED = True if MAILCHIMP_KEY else False

# The Woocommerce plugin won't work until we migrate it from Celery to Django Q2
# This is why its always disabled for now
PLUGIN_WOOCOMMERCE_ENABLED = False


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django_extensions",
    "storages",
    "guardian",
    "rest_framework",
    "rest_framework_tricks",
    "rest_framework.authtoken",
    # "jazzmin",
    "django.contrib.admin",
    "corsheaders",
    "django_filters",
    # "crispy_forms",  # doesn't seem to be used
    # "silk",
    "djoser",
    "django_q",
    "api",
    "plugin_mailchimp",
]

if PLUGIN_WOOCOMMERCE_ENABLED:
    INSTALLED_APPS.append("plugin_woocommerce")

if not (USE_S3 or USE_AZURE):
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")


sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE"),
    environment=env("SENTRY_ENVIRONMENT")
)

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "paul_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "paul_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)


# Django Q2
# https://django-q2.readthedocs.io/en/master/brokers.html

Q_CLUSTER = {
    "name": "paul",
    "workers": env("BACKGROUND_WORKERS"),
    "recycle": 100,
    "timeout": 240,  # All tasks must finish in less than 4 minutes
    "retry": 360,  # Retry unfinished tasks after 6 minutes
    "ack_failures": True,
    "max_attempts": 5,
    "compress": True,
    "save_limit": 200,
    "queue_limit": 4,
    "cpu_affinity": 1,
    "label": "Django Q2",
    "orm": "default",
    "poll": 2,
    "guard_cycle": 3,
    "catch_up": False,  # https://django-q2.readthedocs.io/en/latest/schedules.html#missed-schedules
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE")

TIME_ZONE = env("TIME_ZONE")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LANGUAGES = [
    ("ro", _("Romanian")),
    ("en", _("English")),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

PUBLIC_STATIC_LOCATION = "static"
PUBLIC_MEDIA_LOCATION = "media"

STATIC_URL = "/api/static/"
MEDIA_URL = "/api/media/"

if IS_CONTAINERIZED:
    STATIC_ROOT = "/var/www/paul-api/static"  # noqa
    MEDIA_ROOT = "/var/www/paul-api/media"  # noqa
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATICFILES_DIRS = ()

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if USE_S3:
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{env("AWS_SUBDOMAIN")}'
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_S3_FILE_OVERWRITE = False

    # s3 public media settings
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
elif USE_AZURE:
    # https://django-storages.readthedocs.io/en/latest/backends/azure.html
    AZURE_ACCOUNT_NAME = env("AZURE_ACCOUNT_NAME")
    AZURE_ACCOUNT_KEY = env("AZURE_ACCOUNT_KEY")
    AZURE_CONTAINER = env("AZURE_CONTAINER")
    AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"

    # azure public media settings
    MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
    STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "ORDERING_PARAM": "__order",
}


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"  # TODO: check this!


CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880


# How to handle the unique fields of a table
# Compound constraint is the original method which we don't use anymore (for now)
USE_COMPOUND_CONSTRAINT = False

SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "SET_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "account/activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "account/reset-password/{uid}/{token}",
    "SEND_CONFIRMATION_EMAIL": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PERMISSIONS": {
        "user_create": ["api.permissions.NoPermission"],  # Basically disable user creation through Djoser
    }
}


DEFAULT_FROM_EMAIL = env("NO_REPLY_EMAIL")
SERVER_EMAIL = env("NO_REPLY_EMAIL")
NO_REPLY_EMAIL = env("NO_REPLY_EMAIL")

try:
    SENDGRID_API_KEY = env("SENDGRID_API_KEY")
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
    SENDGRID_ECHO_TO_STDOUT = False
except environ.ImproperlyConfigured:
    EMAIL_BACKEND = env("EMAIL_BACKEND")
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env("EMAIL_USE_TLS")


# Admin config
DJANGO_ADMIN_EMAIL = env("DJANGO_ADMIN_EMAIL")
DJANGO_ADMIN_PASSWORD = env("DJANGO_ADMIN_PASSWORD")
FRONTEND_DOMAIN = env("FRONTEND_DOMAIN")
ADMIN_SITE_TITLE = env("ADMIN_SITE_TITLE")
ADMIN_SITE_HEADER = env("ADMIN_SITE_HEADER")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# django-jazzmin
# -------------------------------------------------------------------------------
# django-jazzmin - https://django-jazzmin.readthedocs.io/configuration/

JAZZMIN_SETTINGS: Dict[str, Any] = {
    # title of the window
    "site_title": ADMIN_SITE_TITLE,
    # Title on the brand, and the login screen (19 chars max)
    "site_header": ADMIN_SITE_HEADER,
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    # "site_logo": "jazzmin/img/logomark.svg",
    # "site_logo_short": "jazzmin/img/logomark.svg",
    # "site_icon": "jazzmin/img/logomark.svg",
    # "site_logo_classes": "site-logo",
    # Welcome text on the login screen
    "welcome_sign": "",
    # Copyright on the footer
    "copyright": "Code4Romania",
    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "donors.Donor",
    # The field name on user model that contains avatar image
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"model": "auth.user", "new_window": False},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to auto expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["pages", "sites"],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "api",
        "api.chart",
        "api.entry",
        "api.database",
        "api.table",
        "api.filterjointable",
        "api.filter",
        "api.csvimport",
        "plugin_mailchimp",
        "plugin_mailchimp.settings",
        "plugin_mailchimp.task",
        "plugin_mailchimp.taskresult",
        "plugin_woocommerce",
        "plugin_woocommerce.settings",
        "plugin_woocommerce.task",
        "plugin_woocommerce.taskresult",
        "authtoken",
        "authtoken.tokenproxy",
        "auth",
        "auth.user",
        "auth.group",
    ],
    # Custom icons for side menu apps/models
    # See https://fontawesome.com/v5/search?m=free
    # for a list of icon classes
    "icons": {
        "api.chart": "fas fa-chart-bar",
        "api.csvimport": "fas fa-file-csv",
        "api.database": "fas fa-database",
        "api.entry": "fas fa-file-alt",
        "api.filter": "fas fa-filter",
        "api.filterjointable": "fas fa-border-all",
        "api.table": "fas fa-table",
        "auth.group": "fas fa-users",
        "auth.user": "fas fa-user",
        "authtoken.tokenproxy": "fas fa-fingerprint",
        "plugin_mailchimp.settings": "fas fa-cogs",
        "plugin_mailchimp.task": "fas fa-tasks",
        "plugin_mailchimp.taskresult": "fas fa-check-double",
        "plugin_woocommerce.settings": "fas fa-cogs",
        "plugin_woocommerce.task": "fas fa-tasks",
        "plugin_woocommerce.taskresult": "fas fa-check-double",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "jazzmin/css/admin.css",
    "custom_js": "",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": DEBUG,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "single",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser": True,
}

if not DEBUG:
    JAZZMIN_SETTINGS["usermenu_links"].extend(
        [
            {
                "name": "Configuration",
                "url": "https://django-jazzmin.readthedocs.io/configuration/",
                "new_window": True,
                "icon": "fas fa-wrench",
            },
            {
                "name": "Support",
                "url": "https://github.com/farridav/django-jazzmin/issues",
                "new_window": True,
                "icon": "fas fa-question",
            },
        ]
    )

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}

LOGIN_URL='/api/admin/login/'


LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'verbose': {
           'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
       },
   },
   'handlers': {
       'console': {
           'level': 'DEBUG',
           'class': 'logging.StreamHandler',
           'stream': sys.stdout,
           'formatter': 'verbose'
       },
   },
   'loggers': {
       '': {
           'handlers': ['console'],
           'level': 'WARNING',
           'propagate': True,
       },
   },
}
