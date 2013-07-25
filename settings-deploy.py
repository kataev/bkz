# -*- coding: utf-8 -*-
from bkz.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'bkz', # Or path to database file if using sqlite3.
    'USER': 'bkz', # Not used with sqlite3.
    'PASSWORD': 'bkz', # Not used with sqlite3.
    'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
}

STATIC_ROOT = '/var/www/bkz/static/'#diff --git a/settings.py b/settings.py
DATABASES['old'] = {
    'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'disp', # Or path to database file if using sqlite3.
    'USER': 'root', # Not used with sqlite3.
    'PASSWORD': '89026441284', # Not used with sqlite3.
    'HOST': 'server', # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '', # Set to empty string for default. Not used with sqlite3.
}
