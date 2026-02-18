"""
Django dev settings with SQLite for local testing without Docker/Postgres.
"""
from support_backend.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
