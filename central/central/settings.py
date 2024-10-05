"""
Django settings for central project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path

from django.core.management.utils import get_random_secret_key  


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Loading environmental variables
load_dotenv(os.environ.get("VARIABLES_PATH"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.environ.get("SERVER_IP"), "localhost", "boolhub"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap5",
    "constance",
    "devices.apps.DevicesConfig",
    "rooms.apps.RoomsConfig",
    "lighting.apps.LightingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "central.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "website", "templates")],
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

WSGI_APPLICATION = "central.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "central",
        "USER": os.environ.get("POSTGRE_USER"),
        "PASSWORD": os.environ.get("POSTGRE_PASSWORD"),
        "HOST": "postgresql",
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pl"

TIME_ZONE = "CET"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Constance configuration
# https://django-constance.readthedocs.io/en/latest/

CONSTANCE_BACKEND = "constance.backends.redisd.RedisBackend"

CONSTANCE_REDIS_CONNECTION = {
    "host": "redis",
    "password": os.environ.get("REDIS_PASSWORD"),
    "port": 6379,
    "db": 0,
}

CONSTANCE_CONFIG = {
    "Powiadamiaj o temperaturze": (False, "", bool),
    "Powiadamiaj o wilgotności": (False, "", bool),
    "Powiadamiaj o zanieczyszczeniu": (False, "", bool),
    "Powiadamiaj o diagnostyce urządzeń": (False, "", bool),
    "Powiadamiaj o przeciążeniu sieci": (False, "", bool),
    "Powiadamiaj o nieznanym urządzeniu w sieci": (False, "", bool),
    "Minimalna temperatura": (19.0, "", float),
    "Maksymalna temperatura": (27.0, "", float),
    "Maksymalna wilgotność": (85, "", int),
    "Minimalna wilgotność": (20, "", int),
    "Próg zanieczyszczenia": (50, "", int),
    "Minimalny poziom baterii/filtra": (15, "", int),
    "Próg przeciążenia sieci": (10, "", int),
    "NTFY URL": ("", "", str),
    "WEATHER API URL": ("", "", str),
    "LATITUDE": ("", "", str),
    "LONGITUDE": ("", "", str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Sieć": (
        "Powiadamiaj o przeciążeniu sieci",
        "Powiadamiaj o nieznanym urządzeniu w sieci",
        "Próg przeciążenia sieci",
    ),
    "Temperatura": (
        "Powiadamiaj o temperaturze",
        "Minimalna temperatura",
        "Maksymalna temperatura",
    ),
    "Wilgotność": (
        "Powiadamiaj o wilgotności",
        "Maksymalna wilgotność",
        "Minimalna wilgotność",
    ),
    "Zanieczyszczenie": ("Powiadamiaj o zanieczyszczeniu", "Próg zanieczyszczenia"),
    "Diagnostyka": (
        "Powiadamiaj o diagnostyce urządzeń",
        "Minimalny poziom baterii/filtra",
    ),
    "NTFY": {"NTFY URL"},
    "WEATHER API": {"WEATHER API URL", "LATITUDE", "LONGITUDE"},
}