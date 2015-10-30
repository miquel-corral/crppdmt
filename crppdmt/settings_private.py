"""
Django settings for crppdmt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
from crppdmt.constants import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'urk$y)-v%z=65jf@e@7_zg*h=ne)s3c^&14plbw(#hrctdpxnm'

# Control vars
DEBUG = True # django
DEPLOY_ENV = os.getenv("DEPLOY_ENV", LOCAL)
MY_DEBUG = os.getenv("MY_DEBUG", OFF)  # my_own purpose
TEST = os.getenv("TEST", OFF)
EMAIL = os.getenv("EMAIL", ON)
FTP = os.getenv("FTP", ON)

# watch ALLOWED_HOSTS in production mode
if DEPLOY_ENV == REMOTE:
    SMT_URL = "https://crppdmt.herokuapp.com/"
    DEBUG = True
    ALLOWED_HOSTS = ["https://crppdmt.herokuapp.com/"]
else:
    SMT_URL = "http://localhost:5000/"
    DEBUG = True
    ALLOWED_HOSTS = ['*']

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

if DEPLOY_ENV == REMOTE:
    DATABASES['default'] = dj_database_url.config()

# email settings
EMAIL_HOST = 'mail.cityresilience.org'
EMAIL_HOST_USER = 'secondments@cityresilience.org'
EMAIL_HOST_PASSWORD = 'miquel03'
DEFAULT_FROM_EMAIL = 'secondments@cityresilience.org'
SERVER_EMAIL = 'secondments@cityresilience.org'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
SECONDMENTS_MAIL_LIST = ['secondments@cityresilience.org',]
UNHABITAT_MAIL_LIST = ['Andre.Dzikus@unhabitat.org', 'David.Evans@unhabitat.org', 'Marcella.Rouweler@unhabitat.org',
                       'Amrita.Jaidka@unhabitat.org',]


# FTP Details
FTP_HOST = "cityresilience.org"
FTP_USER = "cityresilience"
FTP_PASS = "Mike2003"
FTP_PORT = 21
FTP_BASE_DIR = "crppdmtfiles"

################################################
#
# NORCAP email addresses
#
################################################
EMAIL_ADDRESS_NORCAP = "request.norcap@nrc.no"


NORCAP_EMAILS = {
    PROFILE_FOOD_SECURITY: "astrid.tveteraas@nrc.no",
    PROFILE_DRR: "astrid.tveteraas@nrc.no",
    PROFILE_SHELTER: "nasrin.omer@nrc.no",
    PROFILE_ENGINEERING: "nasrin.omer@nrc.no",
    PROFILE_WATER: "nasrin.omer@nrc.no",
    PROFILE_SANITATON: "nasrin.omer@nrc.no",
    PROFIlE_EDUCATION: "ingvill.tveite@nrc.no",
    PROFILE_NUTRITION: "ingvill.tveite@nrc.no",
    PROFILE_HEALTH: "ingvill.tveite@nrc.no",
    PROFILE_COMMUNICATION: "hkp@nrc.no",
    PROFILE_COORDINATION: "hkp@nrc.no",
    PROFILE_STATISTICS: "hkp@nrc.no",
    PROFILE_CHILD_PROTECTION: "anne.hoseth@nrc.no",
    PROFILE_GENDER: "anne.hoseth@nrc.no",
    PROFILE_CAMP_COORDINATION: "jorn.owre@nrc.no",
    PROFILE_HOUSING: "linn.bogsnes.miles@nrc.no",
    PROFILE_ICT: "erlend.hvoslef@nrc.no",
    PROFILE_LOGISTICS: "erlend.hvoslef@nrc.no",
    PROFILE_INFORMATION_MANAGEMENT: "erlend.hvoslef@nrc.no",
    PROFILE_PROJECT_FORMULATION: "jorn.owre@nrc.no",
}

NORCAP_FOCAL_POINTS = {
    PROFILE_FOOD_SECURITY: "Astrid",
    PROFILE_DRR: "Astrid",
    PROFILE_SHELTER: "Nasrin",
    PROFILE_ENGINEERING: "Nasrin",
    PROFILE_WATER: "Nasrin",
    PROFILE_SANITATON: "Nasrin",
    PROFIlE_EDUCATION: "Ingvill",
    PROFILE_NUTRITION: "Ingvill",
    PROFILE_HEALTH: "Ingvill",
    PROFILE_COMMUNICATION: "Helen",
    PROFILE_COORDINATION: "Helen",
    PROFILE_STATISTICS: "Helen",
    PROFILE_CHILD_PROTECTION: "Anne",
    PROFILE_GENDER: "Anne",
    PROFILE_CAMP_COORDINATION: "Jorn",
    PROFILE_HOUSING: "Linn",
    PROFILE_ICT: "Erlend",
    PROFILE_LOGISTICS: "Erlend",
    PROFILE_INFORMATION_MANAGEMENT: "Erlend",
    PROFILE_PROJECT_FORMULATION: "Jorn",
}