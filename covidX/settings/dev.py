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
