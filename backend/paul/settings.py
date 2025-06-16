"""
Django settings for the backend project.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import hashlib
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import environ
import sentry_sdk
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.encoder import CustomJsonEncoder


# Constants for memory sizes
KIBIBYTE = 1024
MEBIBYTE = KIBIBYTE * 1024
GIBIBYTE = MEBIBYTE * 1024
TEBIBYTE = GIBIBYTE * 1024


# Environment parameters
root = Path(__file__).resolve().parent.parent.parent

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.abspath(os.path.join(root, "backend"))


env = environ.Env(
    # aws settings
    AWS_REGION_NAME=(str, ""),
    AWS_S3_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_DEFAULT_ACL=(str, "private"),
    AWS_S3_DEFAULT_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_DEFAULT_PREFIX=(str, ""),
    AWS_S3_PUBLIC_ACL=(str, "public-read"),
    AWS_S3_PUBLIC_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_PUBLIC_PREFIX=(str, ""),
    AWS_S3_REGION_NAME=(str, ""),
    AWS_S3_STORAGE_DEFAULT_BUCKET_NAME=(str, ""),
    AWS_S3_STORAGE_PUBLIC_BUCKET_NAME=(str, ""),
    AWS_SES_CONFIGURATION_SET_NAME=(str, None),
    AWS_SES_INCLUDE_REPORTS=(bool, False),
    AWS_SES_REGION_NAME=(str, ""),
    USE_S3=(bool, False),
    # azure settings
    AZURE_ACCOUNT_KEY=(str, ""),
    AZURE_ACCOUNT_NAME=(str, ""),
    AZURE_CONTAINER=(str, "data"),
    USE_AZURE=(bool, False),
    # django settings
    ALLOWED_HOSTS=(list, ["*"]),
    CORS_ALLOW_ALL_ORIGINS=(bool, False),
    CORS_ALLOWED_ORIGINS=(list, []),
    DATA_UPLOAD_MAX_MEMORY_SIZE=(int, 3 * MEBIBYTE),
    DEBUG=(bool, False),
    DJANGO_VITE_DEV_MODE=(bool, False),
    DJANGO_VITE_DEV_SERVER_PORT=(int, 3000),
    ENABLE_2FA=(bool, False),
    ENABLE_CACHE=(bool, False),
    ENABLE_DJANGO_ADMIN=(bool, False),
    IS_CONTAINERIZED=(bool, False),
    LANGUAGE_CODE=(str, "ro"),
    LOGLEVEL=(str, "INFO"),
    MAX_DOCUMENT_SIZE=(int, 2 * MEBIBYTE),
    THROTTLE_IP_SIGNUPS_PER_HOUR=(int, 90),  # 0 = disabled
    SECRET_KEY=(str, "secret"),
    SESSION_COOKIE_SECURE=(bool, True),
    SESSION_EXPIRY_IDLE_SECONDS=(int, 4 * 60 * 60),
    TIME_ZONE=(str, "Europe/Bucharest"),
    # db settings
    DATABASE_ENGINE=(str, "sqlite3"),
    DATABASE_HOST=(str, "localhost"),
    DATABASE_NAME=(str, "default"),
    DATABASE_PASSWORD=(str, ""),
    DATABASE_PORT=(str, "3306"),
    DATABASE_USER=(str, "root"),
    # email settings
    CC_STATUS_EMAIL=(str, ""),
    DEFAULT_FROM_EMAIL=(str, "email@example.com"),
    DEFAULT_RECEIVE_EMAIL=(str, "email@example.com"),
    EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
    EMAIL_FAIL_SILENTLY=(bool, False),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_SEND_METHOD=(str, "async"),
    EMAIL_USE_TLS=(str, ""),
    NO_REPLY_EMAIL=(str, "noreply@example.com"),
    # background workers settings
    BACKGROUND_WORKERS_COUNT=(int, 1),
    # recaptcha settings
    RECAPTCHA_PRIVATE_KEY=(str, ""),
    RECAPTCHA_PUBLIC_KEY=(str, ""),
    RECAPTCHA_REQUIRED_SCORE=(float, 0.7),
    # sentry
    SENTRY_DSN=(str, ""),
    SENTRY_PROFILES_SAMPLE_RATE=(float, 0),
    SENTRY_TRACES_SAMPLE_RATE=(float, 0),
    # security expiration dates
    AUDITLOG_EXPIRY_DAYS=(int, 5 * 365),  # 5 years
    EMAIL_VERIFICATION_EXPIRY_HOURS=(int, 96),  # 4 days
    EMAIL_2FA_EXPIRY_HOURS=(int, 4),
    EMAIL_PASSWORD_RESET_EXPIRY_HOURS=(int, 4),
)


# Load parameters from the .env file
dot_env_path = os.path.abspath(os.path.join(root, ".env"))
environ.Env.read_env(dot_env_path)


# SECURITY WARNING: keep the secret key used in production secret
SECRET_KEY = env("SECRET_KEY")
SECRET_KEY_HASH = hashlib.sha256(f"{SECRET_KEY}".encode()).hexdigest()

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE")
SESSION_COOKIE_AGE = env.int("SESSION_EXPIRY_IDLE_SECONDS")  # This also expires the actual session data (from db)
SESSION_SAVE_EVERY_REQUEST = True


# Prevent abuse by enforcing some limits
# THROTTLE_IP_SIGNUPS_PER_HOUR = env.int("THROTTLE_IP_SIGNUPS_PER_HOUR")


# SECURITY WARNING: don't run with debug turned on in production
DEBUG = env.bool("DEBUG")
ENVIRONMENT = env.str("ENVIRONMENT", "production")


# some settings will be different if it's not running in a container (e.g., locally, on a Mac)
IS_CONTAINERIZED = env.bool("IS_CONTAINERIZED")

VERSION = env.str("VERSION", "edge")
REVISION = env.str("REVISION", "develop")

if IS_CONTAINERIZED and VERSION == "edge" and REVISION == "develop":
    version_file = "/var/www/paul/.version"
    if os.path.exists(version_file):
        with open(version_file) as f:
            VERSION, REVISION = f.read().strip().split("+")
            REVISION = REVISION[:7]


# Django logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{asctime}] [{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env.str("LOGLEVEL"),
    },
}


# Sentry
if env.str("SENTRY_DSN"):
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
        release=f"paul@{VERSION}+{REVISION}",
    )


ALLOW_PAST_DATES = env.bool("ALLOW_PAST_DATES", default=DEBUG)

ENABLE_DJANGO_ADMIN = env.bool("ENABLE_DJANGO_ADMIN", default=DEBUG)


# Auditlog configuration

AUDITLOG_EXPIRY_DAYS = env.int("AUDITLOG_EXPIRY_DAYS")
AUDITLOG_INCLUDE_ALL_MODELS = True
AUDITLOG_EXCLUDE_TRACKING_FIELDS = (
    "created_at",
    "updated_at",
)
AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    "auth.Group",
    "django_q",
    "sessions",
)


# superuser/admin seed data

DJANGO_ADMIN_PASSWORD = env.str("DJANGO_ADMIN_PASSWORD", None)
DJANGO_ADMIN_EMAIL = env.str("DJANGO_ADMIN_EMAIL", None)

SEED_ADMIN_PASSWORD = env.str("SEED_ADMIN_PASSWORD", None)
SEED_ADMIN_EMAIL = env.str("SEED_ADMIN_EMAIL", None)


SILENCED_SYSTEM_CHECKS = (
    "urls.W005",  # Ignore duplicate namespace warnings because we use the same namespace for both normal and staff URLs
)


# Security settings

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS")


# Application definition

USE_S3 = env.bool("USE_S3")
USE_AZURE = env.bool("USE_AZURE") and env("AZURE_ACCOUNT_NAME") and env("AZURE_ACCOUNT_KEY")
AWS_SES_INCLUDE_REPORTS = env.bool("AWS_SES_INCLUDE_REPORTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # Third party apps:
    "auditlog",
    "corsheaders",
    "django_q",
    "django_recaptcha",
    "django_vite",
    "inertia",
    "localflavor",
    "storages",
    # paul apps:
    "hello",
    "users",
]

if not (USE_S3 or USE_AZURE):
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

if AWS_SES_INCLUDE_REPORTS:
    INSTALLED_APPS.append("django_ses")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.locale.LocaleMiddleware",  # We use only the Romanian locale
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "inertia.middleware.InertiaMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
    # paul middlewares:
    "users.middleware.global_state",  # noqa
]

ROOT_URLCONF = "paul.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.abspath(os.path.join(BASE_DIR, "templates"))],
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

WSGI_APPLICATION = "paul.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_ENGINE = env("DATABASE_ENGINE")

REMOTE_DATABASE_ENGINES = {
    "mysql": "django.db.backends.mysql",
    "postgresql": "django.db.backends.postgresql",
}
if DATABASE_ENGINE in REMOTE_DATABASE_ENGINES.keys():
    DATABASES = {
        "default": {
            "ENGINE": REMOTE_DATABASE_ENGINES[DATABASE_ENGINE],
            "NAME": env("DATABASE_NAME"),
            "USER": env("DATABASE_USER"),
            "PASSWORD": env("DATABASE_PASSWORD"),
            "HOST": env("DATABASE_HOST"),
            "PORT": env("DATABASE_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.abspath(os.path.join(BASE_DIR, ".db_sqlite", "db.sqlite3")),
        }
    }


CACHE_TIMEOUT_SMALL = 60 * 2
CACHE_TIMEOUT_STANDARD = 60 * 15
CACHE_TIMEOUT_LARGE = 60 * 60 * 2

ENABLE_CACHE = env.bool("ENABLE_CACHE", default=not DEBUG)
if ENABLE_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "paul_cache_default",
            "TIMEOUT": 600,  # default cache timeout in seconds
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

ENABLE_2FA = env.bool("ENABLE_2FA")

AUTH_USER_MODEL = "users.User"

# Email settings
EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_SEND_METHOD = env.str("EMAIL_SEND_METHOD")

DEFAULT_RECEIVE_EMAIL = env("DEFAULT_RECEIVE_EMAIL")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
NO_REPLY_EMAIL = env("NO_REPLY_EMAIL")
CC_STATUS_EMAIL = env("CC_STATUS_EMAIL")

if EMAIL_BACKEND == "django_ses.SESBackend":
    AWS_SES_CONFIGURATION_SET_NAME = env.str("AWS_SES_CONFIGURATION_SET_NAME")

    AWS_SES_AUTO_THROTTLE = env.float("AWS_SES_AUTO_THROTTLE", default=0.5)
    AWS_SES_REGION_NAME = env.str("AWS_SES_REGION_NAME") if env("AWS_SES_REGION_NAME") else env("AWS_REGION_NAME")
    AWS_SES_REGION_ENDPOINT = env.str("AWS_SES_REGION_ENDPOINT", default=f"email.{AWS_SES_REGION_NAME}.amazonaws.com")

    AWS_SES_FROM_EMAIL = DEFAULT_FROM_EMAIL

    USE_SES_V2 = env.bool("AWS_SES_USE_V2", default=True)

    if aws_access_key := env("AWS_ACCESS_KEY_ID", default=None):
        AWS_ACCESS_KEY_ID = aws_access_key
        AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
else:
    AWS_SES_CONFIGURATION_SET_NAME = None
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

EMAIL_FAIL_SILENTLY = env.bool("EMAIL_FAIL_SILENTLY")

EMAIL_VERIFICATION_EXPIRY_TIME = timezone.timedelta(hours=env.int("EMAIL_VERIFICATION_EXPIRY_HOURS"))
TWO_FACTOR_AUTH_EXPIRY_TIME = timezone.timedelta(hours=env.int("EMAIL_2FA_EXPIRY_HOURS"))
PASSWORD_RESET_EXPIRY_TIME = timezone.timedelta(hours=env.int("EMAIL_PASSWORD_RESET_EXPIRY_HOURS"))

MAX_RESET_ATTEMPTS = 5
MAX_LOGIN_ATTEMPTS = 5

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE")

TIME_ZONE = env("TIME_ZONE")

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

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
        "region_name": env.str("AWS_S3_REGION_NAME") or env.str("AWS_REGION_NAME"),
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

    if custom_domain := env.str("AWS_S3_DEFAULT_CUSTOM_DOMAIN", default=None):
        public_storage_options["custom_domain"] = custom_domain

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

    azure_custom_domain = f'{env("AZURE_ACCOUNT_NAME")}.blob.core.windows.net'
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

# Maximum request size excludind the uploaded files
DATA_UPLOAD_MAX_MEMORY_SIZE = env.int("DATA_UPLOAD_MAX_MEMORY_SIZE")

# Maximum single file size for uploaded files
MAX_DOCUMENT_SIZE = env.int("MAX_DOCUMENT_SIZE")


# Django Vite config

# Where ViteJS assets are built
django_vite_assets_path = os.path.abspath(os.path.join(os.pardir, "frontend", "dist"))  # noqa
django_vite_sources_dir = os.path.abspath(os.path.join(os.pardir, "frontend", "src"))  # noqa

django_vite_dev_mode = env.bool("DJANGO_VITE_DEV_MODE")
django_vite_settings: Dict[str, Any] = {
    "dev_mode": django_vite_dev_mode,
    "manifest_path": os.path.join(django_vite_assets_path, ".vite", "manifest.json"),
}

if IS_CONTAINERIZED:
    # Where ViteJS assets are built
    STATIC_ROOT = os.path.abspath(os.path.join(os.sep, "var", "www", "paul", "backend", "static"))
    MEDIA_ROOT = os.path.abspath(os.path.join(os.sep, "var", "www", "paul", "backend", "media"))


# If we should use HMR or not
if django_vite_dev_mode:
    django_vite_settings["dev_server_port"] = env.int("DJANGO_VITE_DEV_SERVER_PORT")
    STATICFILES_DIRS = [django_vite_sources_dir]
else:
    STATICFILES_DIRS = [django_vite_assets_path]

STATICFILES_DIRS.append(os.path.abspath(os.path.join(BASE_DIR, "static_extras")))

DJANGO_VITE: Dict[str, Dict] = {
    "default": django_vite_settings,
}


# InertiaJS

INERTIA_JSON_ENCODER = CustomJsonEncoder

INERTIA_VERSION = "1.0"  # defaults to '1.0'
INERTIA_LAYOUT = "base.html"  # required and has no default
INERTIA_SSR_URL = env.str("INERTIA_SSR_URL", default="http://localhost:13714")
INERTIA_SSR_ENABLED = env.bool("INERTIA_SSR_ENABLED", default=django_vite_dev_mode)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django Q2
# https://django-q2.readthedocs.io/en/stable/brokers.html

Q_CLUSTER = {
    "name": "paul",
    "workers": env.int("BACKGROUND_WORKERS_COUNT"),
    "recycle": 100,
    "timeout": 900,  # A task must finish in less than 15 minutes
    "retry": 1200,  # Retry an unfinished tasks after 20 minutes
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


# reCAPTCHA

RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_REQUIRED_SCORE = env("RECAPTCHA_REQUIRED_SCORE")

RECAPTCHA_ENABLED = True if RECAPTCHA_PUBLIC_KEY else False
