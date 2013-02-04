# -*- coding: utf-8 -*-
import os, sys
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = False

INTERNAL_IPS = ('127.0.0.1','192.168.1.2','192.168.0.72')
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS' : False}

DEVSERVER_MODULES = ()

WEBODT_CONVERTER = 'webodt.converters.openoffice.OpenOfficeODFConverter'
WEBODT_TEMPLATE_PATH = 'core/templates/'

ADMINS = (('Kataev Denis', 'bteamko@gmail.com'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bkz', # Or path to database file if using sqlite3.
        'USER': 'bkz', # Not used with sqlite3.
        'PASSWORD': 'bkz', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
    },
   # 'default': {
   #     'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': '../bkz_test.db', # Or path to database file if using sqlite3.
   # },
     'old': {
         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': 'disp', # Or path to database file if using sqlite3.
         'USER': 'root', # Not used with sqlite3.
         'PASSWORD': '89026441284', # Not used with sqlite3.
         'HOST': 'server', # Set to empty string for localhost. Not used with sqlite3.
         'PORT': '', # Set to empty string for default. Not used with sqlite3.
     },
    # 'localhost': {
    #     'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    #     'NAME': 'bteam', # Or path to database file if using sqlite3.
    #     'USER': 'root', # Not used with sqlite3.
    #     'PASSWORD': 'root', # Not used with sqlite3.
    #     'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
    #     'PORT': '', # Set to empty string for default. Not used with sqlite3.
    # },
}

SOUTH_TESTS_MIGRATE = False

DATABASE_ROUTERS = ('routes.bkzRouter',)

APPEND_SLASH = True
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Yekaterinburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
    )


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
#USE_L10N = True
FORMAT_MODULE_PATH = 'core.formats'
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/bkz/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static/'),
    'static/'
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f%v!01v02pm%evmp#4v9v4%ocqy+peu*&_3j)*!6in&4)o9n%z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader',(
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#         'django.template.loaders.eggs.Loader',
#    )
#        ),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'bkz.ipaccess.middleware.IPAccessMiddleware',
    'bkz.middleware.Access',
    'linaro_django_pagination.middleware.PaginationMiddleware',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'bkz.context.bricks',
    'bkz.context.namespace',
    )

ROOT_URLCONF = 'bkz.urls'

TEMPLATE_DIRS = (
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.formtools',
    'django.contrib.webdesign',

    'bkz.ipaccess',

    'bkz.old',
    'bkz.core',

    'bkz.cpu',
    'bkz.lab',
    'bkz.make',
    'bkz.whs',
    'bkz.energy',
    'bkz.it',

    'bkz.bootstrap',


    'django_extensions',
    'debug_toolbar',
    'pytils',
    'devserver',
    'south',
    'gunicorn',
#    'piston',
    'webodt',
    'linaro_django_pagination',    
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}
