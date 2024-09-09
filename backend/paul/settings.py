"""
Django settings for paul project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import environ
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _


# Constants for memory sizes
KIBIBYTE = 1024
MEBIBYTE = KIBIBYTE * 1024
GIBIBYTE = MEBIBYTE * 1024
TEBIBYTE = GIBIBYTE * 1024


# Build paths inside the project like this: BASE_DIR / 'subdir'.
root = Path(__file__).resolve().parent.parent.parent
BASE_DIR = os.path.abspath(os.path.join(root, "backend"))


env = environ.Env(
    # aws settings
    USE_S3=(bool, False),
    AWS_REGION_NAME=(str, ""),
    AWS_S3_STORAGE_DEFAULT_BUCKET_NAME=(str, ""),
    AWS_S3_STORAGE_PUBLIC_BUCKET_NAME=(str, ""),
    AWS_S3_DEFAULT_ACL=(str, "private"),
    AWS_S3_PUBLIC_ACL=(str, "public-read"),
    AWS_S3_DEFAULT_PREFIX=(str, ""),
    AWS_S3_PUBLIC_PREFIX=(str, ""),
    AWS_S3_REGION_NAME=(str, ""),
    AWS_S3_DEFAULT_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_PUBLIC_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_CUSTOM_DOMAIN=(str, ""),
    AWS_SES_REGION_NAME=(str, ""),
    AWS_SES_INCLUDE_REPORTS=(bool, False),
    AWS_SES_CONFIGURATION_SET_NAME=(str, None),
    AWS_COGNITO_REGION=(str, ""),
    AWS_COGNITO_DOMAIN=(str, ""),
    AWS_COGNITO_USER_POOL_ID=(str, ""),
    AWS_COGNITO_CLIENT_ID=(str, ""),
    AWS_COGNITO_CLIENT_SECRET=(str, ""),
    # azure settings
    USE_AZURE=(bool, False),
    AZURE_ACCOUNT_NAME=(str, ""),
    AZURE_ACCOUNT_KEY=(str, ""),
    AZURE_CONTAINER=(str, "data"),
    # django settings
    DEBUG=(bool, False),
    ENABLE_DEBUG_TOOLBAR=(bool, False),
    ENVIRONMENT=(str, "production"),
    SECRET_KEY=(str, "replace-with-a-secret-key"),
    LOGLEVEL=(str, "INFO"),
    ALLOWED_HOSTS=(list, ["*"]),
    IS_CONTAINERIZED=(bool, False),
    LANGUAGE_CODE=(str, "ro"),
    TIME_ZONE=(str, "Europe/Bucharest"),
    AUDITLOG_EXPIRY_DAYS=(int, 45),
    DATA_UPLOAD_MAX_MEMORY_SIZE=(int, 3 * MEBIBYTE),
    MAX_DOCUMENT_SIZE=(int, 2 * MEBIBYTE),
    # db settings
    # DATABASE_ENGINE=(str, "sqlite3"),
    DATABASE_NAME=(str, "default"),
    DATABASE_USER=(str, "root"),
    DATABASE_PASSWORD=(str, ""),
    DATABASE_HOST=(str, "localhost"),
    DATABASE_PORT=(str, "5432"),
    # Sentry
    SENTRY_DSN=(str, ""),
    SENTRY_TRACES_SAMPLE_RATE=(float, 0),
    SENTRY_PROFILES_SAMPLE_RATE=(float, 0),
    # django-q2 settings
    BACKGROUND_WORKERS_COUNT=(int, 1),
    # recaptcha settings
    RECAPTCHA_PUBLIC_KEY=(str, ""),
    RECAPTCHA_PRIVATE_KEY=(str, ""),
    # email settings
    EMAIL_SEND_METHOD=(str, "async"),
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_TLS=(str, ""),
    EMAIL_FAIL_SILENTLY=(bool, False),
    DEFAULT_FROM_EMAIL=(str, "no-reply@code4.ro"),
    NO_REPLY_EMAIL=(str, "no-reply@code4.ro"),
    # ngo hub api settings
    NGOHUB_HOME_HOST=(str, "ngohub.ro"),
    NGOHUB_APP_HOST=(str, "app-staging.ngohub.ro"),
    NGOHUB_API_HOST=(str, "api-staging.ngohub.ro"),
    NGOHUB_API_ACCOUNT=(str, ""),
    NGOHUB_API_KEY=(str, ""),
)

# reading .env file
dot_env_path = os.path.abspath(os.path.join(root, ".env"))
environ.Env.read_env(dot_env_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")
ENVIRONMENT = env.str("ENVIRONMENT")
SILENCED_SYSTEM_CHECKS = []

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# some settings will be different if it's not running in a container (e.g., locally, on a Mac)
IS_CONTAINERIZED = env.bool("IS_CONTAINERIZED")

VERSION = env.str("VERSION", "edge")
REVISION = env.str("REVISION", "develop")

if IS_CONTAINERIZED and VERSION == "edge" and REVISION == "develop":
    version_file = "/var/www/votong/.version"
    if os.path.exists(version_file):
        with open(version_file) as f:
            VERSION, REVISION = f.read().strip().split("+")
            REVISION = REVISION[:7]


USE_S3 = env.bool("USE_S3")
USE_AZURE = env.bool("USE_AZURE") and env("AZURE_ACCOUNT_NAME") and env("AZURE_ACCOUNT_KEY")
AWS_SES_INCLUDE_REPORTS = env.bool("AWS_SES_INCLUDE_REPORTS")
AWS_REGION_NAME = env("AWS_REGION_NAME")


# Application definition

INSTALLED_APPS = [
    'unfold',  # this must be loaded before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Authentication:
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.amazon_cognito",
    # PAUL Apps:
    'accounts',
    'datastore',
    'hello',
    'plugin_mailchimp',
    # other third-party
    "storages",
    "django_q",
    # "guardian",
]

if not (USE_S3 or USE_AZURE):
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

if AWS_SES_INCLUDE_REPORTS:
    INSTALLED_APPS.append("django_ses")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # this is the default
    # "guardian.backends.ObjectPermissionBackend",
    "accounts.auth_backends.CaseInsensitiveUserModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = 'paul.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.abspath(os.path.join(BASE_DIR, "templates"))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'paul.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

TIMEOUT_CACHE_SHORT = 60  # 1 minute
TIMEOUT_CACHE_NORMAL = 60 * 15  # 15 minutes
TIMEOUT_CACHE_LONG = 60 * 60 * 2  # 2 hours

ENABLE_CACHE = env.bool("ENABLE_CACHE", default=not DEBUG)
if ENABLE_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "paul_cache_default",
            "TIMEOUT": TIMEOUT_CACHE_NORMAL,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
CACHES["file_resubmit"] = {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": "/tmp/file_resubmit/",
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LANGUAGE_CODE = env("LANGUAGE_CODE")

LANGUAGES = (
    ("en", "English"),
    ("ro", "Română"),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

# superuser/admin seed data
DJANGO_ADMIN_PASSWORD = env.str("DJANGO_ADMIN_PASSWORD", None)
DJANGO_ADMIN_EMAIL = env.str("DJANGO_ADMIN_EMAIL", None)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

public_static_location = "static"
public_media_location = "media"
private_media_location = "media"

STATIC_URL = f"{public_static_location}/"
MEDIA_URL = f"{public_media_location}/"

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "static"))
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "media"))

media_storage = "django.core.files.storage.FileSystemStorage"
static_storage = "whitenoise.storage.CompressedStaticFilesStorage"

default_storage_options = {}
public_storage_options = {}

if env.bool("USE_S3"):
    media_storage = "storages.backends.s3boto3.S3Boto3Storage"
    static_storage = "storages.backends.s3boto3.S3StaticStorage"

    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    default_storage_options = {
        "bucket_name": (env.str("AWS_S3_STORAGE_DEFAULT_BUCKET_NAME")),
        "default_acl": (env.str("AWS_S3_DEFAULT_ACL")),
        "region_name": env.str("AWS_S3_REGION_NAME") or AWS_REGION_NAME,
        "object_parameters": {"CacheControl": "max-age=86400"},
        "file_overwrite": False,
    }

    if aws_session_profile := env.str("AWS_S3_SESSION_PROFILE", default=None):
        default_storage_options["session_profile"] = aws_session_profile
    elif aws_access_key := env.str("AWS_ACCESS_KEY_ID", default=None):
        default_storage_options["access_key"] = aws_access_key
        default_storage_options["secret_key"] = env.str("AWS_SECRET_ACCESS_KEY")

    if default_prefix := env.str("AWS_S3_DEFAULT_PREFIX", default=None):
        default_storage_options["location"] = default_prefix

    if custom_domain := (
        env.str("AWS_S3_CUSTOM_DOMAIN", default=None) or env.str("AWS_S3_DEFAULT_CUSTOM_DOMAIN", default=None)
    ):
        default_storage_options["custom_domain"] = custom_domain

    public_storage_options = deepcopy(default_storage_options)
    if public_acl := env.str("AWS_S3_PUBLIC_ACL"):
        public_storage_options["default_acl"] = public_acl
    if public_bucket_name := env.str("AWS_S3_STORAGE_PUBLIC_BUCKET_NAME"):
        public_storage_options["bucket_name"] = public_bucket_name
    if public_prefix := env.str("AWS_S3_PUBLIC_PREFIX", default=None):
        public_storage_options["location"] = public_prefix
    if custom_domain := (
        env.str("AWS_S3_CUSTOM_DOMAIN", default=None) or env.str("AWS_S3_PUBLIC_CUSTOM_DOMAIN", default=None)
    ):
        public_storage_options["custom_domain"] = custom_domain
elif USE_AZURE:
    media_storage = "storages.backends.azure_storage.AzureStorage"
    static_storage = "storages.backends.azure_storage.AzureStorage"

    # https://django-storages.readthedocs.io/en/latest/backends/azure.html
    if azure_connection_string := env("AZURE_CONNECTION_STRING", default=None):
        default_storage_options["connection_string"] = azure_connection_string
    else:
        default_storage_options["account_name"] = env("AZURE_ACCOUNT_NAME")
        default_storage_options["account_key"] = env("AZURE_ACCOUNT_KEY")

    default_storage_options["azure_container"] = env("AZURE_CONTAINER")

    azure_custom_domain = f"{env('AZURE_ACCOUNT_NAME')}.blob.core.windows.net"
    default_storage_options["custom_domain"] = azure_custom_domain

    # azure public media settings
    MEDIA_URL = f"https://{azure_custom_domain}/{public_media_location}/"

STORAGES = {
    "default": {
        "BACKEND": media_storage,
        "LOCATION": private_media_location,
        "OPTIONS": default_storage_options,
    },
    "public": {
        "BACKEND": media_storage,
        "LOCATION": public_media_location,
        "OPTIONS": public_storage_options,
    },
    "staticfiles": {
        "BACKEND": static_storage,
        "LOCATION": public_static_location,
        "OPTIONS": public_storage_options,
    },
}

if IS_CONTAINERIZED:
    STATIC_ROOT = os.path.abspath(os.path.join(os.sep, "var", "www", "votong", "backend", "static"))
    MEDIA_ROOT = os.path.abspath(os.path.join(os.sep, "var", "www", "votong", "backend", "media"))

# Maximum request size excludind the uploaded files
DATA_UPLOAD_MAX_MEMORY_SIZE = env.int("DATA_UPLOAD_MAX_MEMORY_SIZE")

# Maximum single file size for uploaded files
MAX_DOCUMENT_SIZE = env.int("MAX_DOCUMENT_SIZE")

STATICFILES_DIRS = (os.path.abspath(os.path.join(BASE_DIR, "static_extras")),)


# Email settings
EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_SEND_METHOD = env.str("EMAIL_SEND_METHOD")
EMAIL_FAIL_SILENTLY = env.bool("EMAIL_FAIL_SILENTLY")

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = env.str("CONTACT_EMAIL", default=DEFAULT_FROM_EMAIL)
NO_REPLY_EMAIL = env.str("NO_REPLY_EMAIL")

if EMAIL_BACKEND == "django_ses.SESBackend":
    AWS_SES_CONFIGURATION_SET_NAME = env.str("AWS_SES_CONFIGURATION_SET_NAME")

    AWS_SES_AUTO_THROTTLE = env.float("AWS_SES_AUTO_THROTTLE", default=0.5)
    AWS_SES_REGION_NAME = env.str("AWS_SES_REGION_NAME") if env("AWS_SES_REGION_NAME") else AWS_REGION_NAME
    AWS_SES_REGION_ENDPOINT = env.str("AWS_SES_REGION_ENDPOINT", default=f"email.{AWS_SES_REGION_NAME}.amazonaws.com")

    AWS_SES_FROM_EMAIL = DEFAULT_FROM_EMAIL

    USE_SES_V2 = env.bool("AWS_SES_USE_V2", default=True)

    if aws_access_key := env("AWS_ACCESS_KEY_ID", default=None):
        AWS_ACCESS_KEY_ID = aws_access_key
        AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
else:
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")


# Django Q2
# https://django-q2.readthedocs.io/en/stable/brokers.html

Q_CLUSTER = {
    "name": "paul",
    "workers": env.int("BACKGROUND_WORKERS_COUNT"),
    "recycle": 100,
    "timeout": 900,  # A task must finish in less than 15 minutes
    "retry": 1200,  # Retry an unfinished task after 20 minutes
    "ack_failures": True,
    "max_attempts": 2,
    "compress": True,
    "save_limit": 200,
    "queue_limit": 4,
    "cpu_affinity": 1,
    "label": _("Background Tasks"),
    "orm": "default",
    "poll": 2,
    "guard_cycle": 3,
    "catch_up": False,
}

# LOGIN_URL = reverse_lazy("login")
# LOGIN_REDIRECT_URL = reverse_lazy("home")
# LOGOUT_REDIRECT_URL = reverse_lazy("home")

# Recaptcha settings
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY", default="")
RECAPTCHA_REQUIRED_SCORE = 0.70

if not RECAPTCHA_PUBLIC_KEY:
    SILENCED_SYSTEM_CHECKS.append("captcha.recaptcha_test_key_error")


# Django logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env.str("LOGLEVEL"),
    },
}

# Sentry
# https://docs.sentry.io/platforms/python/integrations/django/

ENABLE_SENTRY = bool(env.str("SENTRY_DSN"))
if ENABLE_SENTRY:
    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE"),
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE"),
        environment=ENVIRONMENT,
        release=f"votong@{VERSION}+{REVISION}",
    )


# Our custom User model uses the email field as user name, and the email is normalized to lowercase on save.
# This is why we must set a lowercase name for Django Guardian's anonymous user object.
# ANONYMOUS_USER_NAME = "anonymoususer"


# # Django Allauth settings
# SOCIALACCOUNT_PROVIDERS = {
#     "amazon_cognito": {
#         "DOMAIN": "https://" + env.str("AWS_COGNITO_DOMAIN"),
#         "EMAIL_AUTHENTICATION": True,  # TODO
#         "VERIFIED_EMAIL": True,  # TODO
#         "APPS": [
#             {
#                 "client_id": env.str("AWS_COGNITO_CLIENT_ID"),
#                 "secret": env.str("AWS_COGNITO_CLIENT_SECRET"),
#             },
#         ],
#     }
# }

# SOCIALACCOUNT_ADAPTER = "hub.social_adapters.UserOrgAdapter"

# # Django Allauth allow only social logins
# SOCIALACCOUNT_ONLY = True
# ACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_STORE_TOKENS = False

# # used for checking that the user has the VotONG app in NGO Hub
# VOTONG_WEBSITE = env("VOTONG_WEBSITE")

# NGO Hub settings
NGOHUB_HOME_HOST = env("NGOHUB_HOME_HOST")
NGOHUB_HOME_BASE = f"https://{env('NGOHUB_HOME_HOST')}/"
NGOHUB_APP_BASE = f"https://{env('NGOHUB_APP_HOST')}/"
NGOHUB_API_BASE = f"https://{env('NGOHUB_API_HOST')}/"
NGOHUB_API_ACCOUNT = env("NGOHUB_API_ACCOUNT")
NGOHUB_API_KEY = env("NGOHUB_API_KEY")

# NGO Hub user roles
NGOHUB_ROLE_SUPER_ADMIN = "super-admin"
NGOHUB_ROLE_NGO_ADMIN = "admin"
NGOHUB_ROLE_NGO_EMPLOYEE = "employee"

# Configurations for the NGO Hub integration
# UPDATE_ORGANIZATION_METHOD = env("UPDATE_ORGANIZATION_METHOD")

AWS_COGNITO_REGION = env("AWS_COGNITO_REGION") or AWS_REGION_NAME
AWS_COGNITO_USER_POOL_ID = env("AWS_COGNITO_USER_POOL_ID")
AWS_COGNITO_CLIENT_ID = env("AWS_COGNITO_CLIENT_ID")
AWS_COGNITO_CLIENT_SECRET = env("AWS_COGNITO_CLIENT_SECRET")

