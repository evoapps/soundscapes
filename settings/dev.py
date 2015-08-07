from .base import *

SECRET_KEY = 'soundscapesevoapps'

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

STATIC_ROOT = Path(DEPLOY_DIR, 'static')
MEDIA_ROOT = Path(DEPLOY_DIR, 'media')

DOWNLOADS_DIR = Path(DEPLOY_DIR, 'downloads')
ANALYSES_DIR = Path(DEPLOY_DIR, 'analyses')
