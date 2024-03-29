"""
Django settings for marketmoods project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0bly_7qglsej@mbf-zo0=d7nmb3dfvk2*fg6kpbjn!k!_j-fbf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'marketmoods'), 'templates'),
    os.path.join(BASE_DIR, 'templates'),
    BASE_DIR,
)

STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'marketmoods'), 'static'),
    BASE_DIR,
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'valence',
    'graphs',
)

BOSS_API_KEY = 'dj0yJmk9cEpaUjdUWlBWZEZmJmQ9WVdrOVVFUTRRMEZXTkdVbWNHbzlNVGswTnpJM05UVTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kNg--'
BOSS_API_SECRET = '265e6cbc321feb97b6e8b7a8fb006a1658687f29'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'marketmoods.urls'

WSGI_APPLICATION = 'marketmoods.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'market_moods_db',
        'USER': 'postgres',
        'PASSWORD': 'pafsign',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
