"""
Django settings for covidX project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import functools
import glob
import os
import sys

from dotenv import load_dotenv

import covidX.gae_settings as gae  # pylint: disable=no-name-in-module
import covidX.utils as utils  # pylint: disable=no-name-in-module

PROJECT_NAME = "covidX"
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.expanduser(BASE_DIR)
join_project_path = functools.partial(os.path.join, PROJECT_ROOT)

# load LOGGER
LOGGER = utils.createLogger(join_project_path("logs.log"))

# load variables values into ENV
ENV = join_project_path(".env")
load_dotenv(ENV, verbose=True, override=True)

sys.path.extend(map(join_project_path, ("apps/", PROJECT_NAME)))

LOGGER.info(f"Starting {PROJECT_NAME} app")
LOGGER.info(f"BASE_DIR= {PROJECT_ROOT}")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 1800,
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# When running on GAE, access from gcp secret manager.
SECRET_KEY = os.getenv("SECRET_KEY", gae.access_secret_key_version())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG_ENV", None))

ALLOWED_HOSTS = [
    allowed_host  # pylint: disable=used-before-assignment
    if DEBUG and (allowed_host := os.getenv("DJANGO_ALLOWED_HOST"))
    else "0.0.0.0"
]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "django_extensions",
    "guardian",
    "graphene_django",
    # TODO(@codecakes): add "algoliasearch_django" when needed,
    "corsheaders",
    "apps.hrm.apps.HrmConfig",
    "apps.apihealth.apps.APIHealthConfig",
    "apps.auth_zero.apps.Auth0LoginConfig",
    "rest_framework",
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

ROOT_URLCONF = "covidX.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": glob.glob(join_project_path("apps/*/templates")),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

WSGI_APPLICATION = "covidX.wsgi.application"

ASGI_APPLICATION = "covidX.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if GAE_APPLICATION := os.getenv("GAE_APPLICATION", None) and (
    CONNECTION_NAME := os.getenv("CONNECTION_NAME", None)
):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": f"/cloudsql/{CONNECTION_NAME}",
            "USER": f'{os.getenv("DB_USER")}',
            "PASSWORD": f'{os.getenv("DB_PWD")}',
            "NAME": f'{os.getenv("DB_NAME")}',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": os.getenv("POSTGRES_DB_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_DB_PORT", "5432"),
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
        },
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # pylint: disable=line-too-long
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = join_project_path("static")
STATIC_URL = "/static/"

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

# SOCIAL AUTH AUTH0 BACKEND CONFIG
SOCIAL_AUTH_TRAILING_SLASH = os.getenv("SOCIAL_AUTH_TRAILING_SLASH")
SOCIAL_AUTH_AUTH0_KEY = os.environ.get("SOCIAL_AUTH_AUTH0_KEY")
SOCIAL_AUTH_AUTH0_SECRET = os.environ.get("SOCIAL_AUTH_AUTH0_SECRET")
SOCIAL_AUTH_AUTH0_SCOPE = ["openid", "profile", "email"]
SOCIAL_AUTH_AUTH0_DOMAIN = os.environ.get("SOCIAL_AUTH_AUTH0_DOMAIN")
SOCIAL_AUTH_ACCESS_TOKEN_METHOD = os.getenv("ACCESS_TOKEN_METHOD")

if AUDIENCE := (
    os.getenv("AUTH0_AUDIENCE") or f"https://{SOCIAL_AUTH_AUTH0_DOMAIN}/userinfo"
):
    SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS = {"audience": AUDIENCE}

AUTHENTICATION_BACKENDS = {
    "apps.auth_zero.auth0backend.Auth0",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONOpenAPIRenderer",
    ],
}

LOGIN_URL = "/auth0/login/auth0"
LOGIN_REDIRECT_URL = "/"

# See: https://django-guardian.readthedocs.io/en/stable/\
# configuration.html#guardian-raise-403
GUARDIAN_RENDER_403 = True

GRAPHENE = {
    "SCHEMA": "covidX.schema.schema",
    "SCHEMA_OUTPUT": "schema.json",
    "SCHEMA_INDENT": 2,
}
ALGOLIA = {
    "APPLICATION_ID": os.getenv("ALGOLIA_APPLICATION_ID"),
    "API_KEY": os.getenv("ALGOLIA_API_KEY"),
}
