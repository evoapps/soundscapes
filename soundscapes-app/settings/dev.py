from .base import *

from os import environ

SECRET_KEY = '-_gv8$ag75vser4gm12mufcxp=ax(=cco1ng&dh70l8ghhi$m+'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'soundscapes',
        'USER': environ.get('DATABASE_USER', 'soundscapes'),
        'PASSWORD': environ.get('DATABASE_PASSWORD', 'soundscapesevoapps'),
        'HOST': 'localhost',
        'PORT': '',
    },
}
