from .base import *

from os import environ

SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['soundscapes.evoapps.xyz', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'soundscapes',
        'USER': environ.get('DATABASE_USER'),
        'PASSWORD': environ.get('DATABASE_PASSWORD'),
        'HOST': environ.get('DATABASE_HOST', '127.0.0.1'),
        'PORT': environ.get('DATABASE_PORT', '5432'),
    },
}

STATIC_ROOT = environ.get('STATIC_ROOT')
MEDIA_ROOT = environ.get('MEDIA_ROOT')
