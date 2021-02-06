# pylint:disable=E0611
from covidX.settings.base import *

CONFIG_FILE = "apps/auth_zero/config/test_config.ini"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # pylint:disable=E0602
        "HOST": os.getenv("POSTGRES_DB_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_DB_PORT", "5432"),
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
    },
}

# pylint:disable=E0601,E0602
ALLOWED_HOSTS = [os.getenv("DJANGO_ALLOWED_HOST")] if DEBUG else ALLOWED_HOSTS

# Debug Toolbar is shown only if your IP address is listed in the INTERNAL_IPS
INTERNAL_IPS = [f"{ALLOWED_HOSTS}:8090"]
ALLOWED_HOST = f"{ALLOWED_HOSTS[0]}"

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

CACHES = {
    **CACHES,
    "memcached": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": [
            f"{ALLOWED_HOST}:11211",
            f"{ALLOWED_HOST}:11212",
            f"{ALLOWED_HOST}:11213",
        ],
    },
}

CACHE_MIDDLEWARE_ALIAS = "memcached"

LOGGER.info("ALLOWED_HOSTS is %s", ALLOWED_HOSTS)
LOGGER.info("DEBUG is %s", DEBUG)
