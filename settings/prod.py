from .base import *

from os import environ

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['soundscapes.evoapps.xyz', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'soundscapes',
        'USER': environ.get('DATABASE_USER'),
        'PASSWORD': environ.get('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    },
}
