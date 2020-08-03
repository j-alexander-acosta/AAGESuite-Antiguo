from .base import *  # noqa
# import raven

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'EKBtun0hsgtjTjViBGJpD5/54Pd7wC51sHDHUGZsbpM='

DEBUG = False

# PRODUCTION_APPS = ['raven.contrib.django.raven_compat']
PRODUCTION_APPS = []

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + PRODUCTION_APPS

ALLOWED_HOSTS = ['ch.unach.cl']


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'carga',
        'USER': 'carga',
        'PASSWORD': 'carga',
        'HOST': '/var/run/postgresql',
    }
}

STATIC_ROOT = '/var/lib/carga/static/'
MEDIA_ROOT = '/var/lib/carga/media/'


# RAVEN_CONFIG = {
#     'dsn': 'https://27acb2e2da0942f4b39671a1bd1b555a:f5d77bcf8fd8400db22710d5c1774bb5@sentry.io/1398653',
# }
