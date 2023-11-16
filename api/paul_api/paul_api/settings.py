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
    ADMIN_SITE_TITLE=(str, "PAUL Admin"),
    ADMIN_SITE_HEADER=(str, "PAUL"),
    MAILCHIMP_KEY=(str, ""),
    # django-q2 settings
    BACKGROUND_WORKERS=(int, 3),
    WORKER_TIMEOUT=(int, 20 * 60),  # All tasks must finish in less than 20 minutes
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
    env.bool("USE_S3") and env("AWS_ACCESS_KEY_ID") and env("AWS_SECRET_ACCESS_KEY") and env("AWS_STORAGE_BUCKET_NAME")
)
USE_AZURE = env.bool("USE_AZURE") and env("AZURE_ACCOUNT_NAME") and env("AZURE_ACCOUNT_KEY")


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
    environment=env("SENTRY_ENVIRONMENT"),
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
    "timeout": env("WORKER_TIMEOUT"),
    "retry": env("WORKER_TIMEOUT") + 120,  # Retry unfinished tasks after 2 more minutes
    "ack_failures": True,
    "max_attempts": 2,
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
    ("ro", _("Română")),
    ("en", _("English")),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

PUBLIC_STATIC_LOCATION = "static"
PUBLIC_MEDIA_LOCATION = "media"

STATIC_URL = "/api/static/"
MEDIA_URL = "/api/media/"

if IS_CONTAINERIZED:
    STATIC_ROOT = "/var/www/paul_api/static"  # noqa
    MEDIA_ROOT = "/var/www/paul_api/media"  # noqa
    # STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    # STATICFILES_DIRS = ()

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


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880


# How to handle the unique fields of a table
# Compound constraint is the original method which we don't use anymore (for now)
USE_COMPOUND_CONSTRAINT = False


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
    },
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


LOGIN_URL = "/api/admin/login/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "stream": sys.stdout, "formatter": "verbose"},
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
