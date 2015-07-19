"""
Django settings for soundscapes project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from unipath import Path

# PROJ_DIR/DEPLOY_DIR/APP_DIR/settings/base.py
APP_DIR = Path(__file__).ancestor(2)
DEPLOY_DIR = APP_DIR.parent
PROJ_DIR = DEPLOY_DIR.parent

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djangobower',
    'crispy_forms',
    'rest_framework',

    'manager',
    'player',
)

# Third party app settings
BOWER_COMPONENTS_ROOT = Path(APP_DIR, 'components')
BOWER_INSTALLED_APPS = (
    'bootstrap#3.3.5',
    'backbone#1.2.1',
    'colorbrewer#1.0.0',
    'jquery#2.1.4',
    'd3#3.5.6',
    'underscore#1.8.3'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'soundscapes.urls'

WSGI_APPLICATION = 'soundscapes.wsgi.application'

TEMPLATE_DIRS = (
    Path(APP_DIR, 'templates'),
)

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
