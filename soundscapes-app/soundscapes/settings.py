"""
Django settings for soundscapes project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from unipath import Path

ROOT_DIR = Path(__file__).ancestor(3)
BASE_DIR = Path(ROOT_DIR, 'soundscapes-app')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-_gv8$ag75vser4gm12mufcxp=ax(=cco1ng&dh70l8ghhi$m+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'episodes',
)

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


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(BASE_DIR, 'soundscapes.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = Path(ROOT_DIR, 'static')
STATICFILES_DIRS = (
    Path(BASE_DIR, 'soundscapes/static'),
)

TEMPLATE_DIRS = (
    Path(BASE_DIR, 'soundscapes/templates'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(ROOT_DIR, 'media')

# Download RSS files to downloads directory, and then
# load them into the models (and MEDIA_ROOT)
DOWNLOADS_DIR = Path(ROOT_DIR, 'downloads')
