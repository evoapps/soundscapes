from .base import *

SECRET_KEY = '-_gv8$ag75vser4gm12mufcxp=ax(=cco1ng&dh70l8ghhi$m+'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(PROJ_DIR, 'soundscapes.sqlite3'),
    }
}

STATIC_ROOT = Path(PROJ_DIR, 'static')
MEDIA_ROOT = Path(PROJ_DIR, 'media')

DOWNLOADS_DIR = Path(PROJ_DIR, 'downloads')
ANALYSES_DIR = Path(PROJ_DIR, 'analyses')
