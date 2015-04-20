"""
Django settings for crppdmt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Control execution environment
deploy_env = os.environ.get('DEPLOY_ENV','LOCAL')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'urk$y)-v%z=65jf@e@7_zg*h=ne)s3c^&14plbw(#hrctdpxnm'

# SECURITY WARNING: don't run with debug turned on in production!
if "LOCAL" == deploy_env:
    DEBUG = True
else:
    DEBUG = False


TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (BASE_DIR + "/templates/crppdmt",)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crppdmt',
    'easy_pdf',
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

ROOT_URLCONF = 'crppdmt.urls'

WSGI_APPLICATION = 'crppdmt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dmt',
        'USER': 'miquel',
        'PASSWORD': 'miquel03',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

if 'HEROKU' == deploy_env:
    DATABASES['default'] = dj_database_url.config()


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../crppdmt/static'),
)

# email settings
EMAIL_HOST = 'mail.cityresilience.org'
EMAIL_HOST_USER = 'miguel.corral@cityresilience.org'
EMAIL_HOST_PASSWORD = 'miquel03'
DEFAULT_FROM_EMAIL = 'miguel.corral@cityresilience.org'
SERVER_EMAIL = 'miguel.corral@cityresilience.org'
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# date input formats
DATE_INPUT_FORMATS = (
    '%d/%m/%Y',  # '25/10/2006'
)