from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TLvsQkkZQZE6pyiva5pmDcOzHvnLVr6CRClpwByCj2g='

DEBUG = True

DEVELOPMENT_APPS = []

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + DEVELOPMENT_APPS

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
