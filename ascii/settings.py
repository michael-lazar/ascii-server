from __future__ import annotations

import os

import environ

env = environ.Env()
env.smart_cast = False

BASE_DIR = os.path.dirname(__file__)

DATA_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", "data"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = env.str("SECRET_KEY", "PLEASE_REPLACE_ME!")
else:
    SECRET_KEY = env.str("SECRET_KEY")
    CSRF_TRUSTED_ORIGINS = [env.str("TRUSTED_ORIGIN")]

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "admin_interface",  # These must come before django.contrib.admin
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_cleanup.apps.CleanupConfig",
    "ascii.core",
    "ascii.fudan",
    "ascii.translations",
    "ascii.textmode",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ascii.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # This gives the core app templates priority over templated defined by third-party
            # apps, which is necessary in order to override django-admin templates.
            "ascii/core/templates",
        ],
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

WSGI_APPLICATION = "ascii.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(DATA_ROOT, "ascii.sqlite3"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS: list[dict] = []

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(DATA_ROOT, "static")
STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# These settings are required by django-admin-interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "apscheduler": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "ascii.core.clients": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

MEDIA_ROOT = os.path.join(DATA_ROOT, "media")
MEDIA_URL = "/media/"
