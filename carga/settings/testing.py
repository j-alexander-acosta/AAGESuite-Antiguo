from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = os.environ.get('DJANGO_DEBUG')

DEVELOPMENT_APPS = []

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + DEVELOPMENT_APPS

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_CSS_HASHING_METHOD = 'content'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
