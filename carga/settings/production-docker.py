from .base import *  # noqa
import raven

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'EKBtun0hsgtjTjViBGJpD5/54Pd7wC51sHDHUGZsbpM='

DEBUG = False

PRODUCTION_APPS = ['raven.contrib.django.raven_compat']

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + PRODUCTION_APPS

ALLOWED_HOSTS = ['aagesuite.unach.cl', 'aagesuite2.unach.cl']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

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

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_CSS_HASHING_METHOD = 'content'

RAVEN_CONFIG = {
    'dsn': 'https://6163e03dcd9a4ab2b38ad9e434d3f83f:d995a96323ad4cab9e566fa3be991234@sentry.unach.cl//19',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}
