from .base import *  # noqa
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

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
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_CSS_HASHING_METHOD = 'content'

STATIC_ROOT = '/var/lib/carga/static/'
MEDIA_ROOT = '/var/lib/carga/media/'

sentry_sdk.init(
    dsn="https://cdae7540ad1f42c9af3bb4aa30aa1fb5@o453173.ingest.sentry.io/5441705",
    integrations=[DjangoIntegration()],
    environment='prod',
    #traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
