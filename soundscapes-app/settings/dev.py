from .base import *

SECRET_KEY = '-_gv8$ag75vser4gm12mufcxp=ax(=cco1ng&dh70l8ghhi$m+'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'soundscapes',
        'USER': 'soundscapes',
        'PASSWORD': 'soundscapes',
        'HOST': 'localhost',
        'PORT': '',
    },
}
