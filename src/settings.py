# -*- coding: utf-8 -*-

# Global settings for sag project.
import os

PROJECT_DIR = os.path.dirname(__file__)
PUBLIC_DIR = os.path.join(PROJECT_DIR, 'public')

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'src', 'users', 'locale'),
    os.path.join(PROJECT_DIR, 'src', 'frontend', 'locale'),
    os.path.join(PROJECT_DIR, 'src', 'storage', 'locale'),
)

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'src.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'src.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'custom_admin', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'fixtures'),
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'plain': {
            'format': '%(asctime)s %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'main_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, '..', 'logs', 'main.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'haystack_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, '..', 'logs', 'haystack.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'sentry_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, '..', 'logs', 'sentry.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'haystack': dict(
            handlers=['haystack_log'],
            level='ERROR',
            propagate=True,
        ),
        'sentry.errors': dict(
            handlers=['sentry_log'],
            level='ERROR',
            propagate=True,
        ),
        'uploader': dict(
            handlers=['main_log'],
            level='ERROR',
            propagate=True,
        )
    }
}

# if DEBUG:
#     LOGGING['loggers']['uploader']['handlers'] += ['console']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',

    'haystack',
    'django_extensions',
    'django_autoslug',
    'south',
    'salmonella',
    'chunks',

    'src.custom_admin',
    'src.frontend',
    'src.users',
    'src.storage',
)

###
# custom_admin
MIDDLEWARE_CLASSES += ('src.custom_admin.middleware.ChangelistPreferencesMiddleware', )

###
# django-admin-tools
INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    ) + INSTALLED_APPS
ADMIN_TOOLS_INDEX_DASHBOARD = 'src.custom_admin.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'src.custom_admin.dashboard.CustomAppIndexDashboard'
ADMIN_MEDIA_PREFIX = '/static/admin/'  # грязный хак
ADMIN_TOOLS_MENU = 'src.custom_admin.dashmenu.CustomMenu'

###
# django-sentry
INSTALLED_APPS += (
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    'sentry.plugins.sentry_servers',
    'sentry.plugins.sentry_sites',
    'sentry.plugins.sentry_urls',
)
MIDDLEWARE_CLASSES += ('sentry.client.middleware.SentryResponseErrorIdMiddleware', )

###
# uploader

INSTALLED_APPS += ('src.uploader', )
TEMPLATE_CONTEXT_PROCESSORS += ('src.uploader.context_processors.settings', )
UPLOADER_LIMIT_DIMENSIONS = True
UPLOADER_USE_ASPECT_RATIO = True
UPLOADER_IMAGE_MAX_WIDTH = 960
UPLOADER_IMAGE_MAX_HEIGHT = 640

###
# easy_thumbnails
INSTALLED_APPS += ('easy_thumbnails', )
THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_ALIASES = {
    '': dict(
        teaser=dict(size=(630, 420), crop=False),
        pro6=dict(size=(300, 200), crop='smart'),
        pro6_gray=dict(size=(300, 200), crop='smart', bw=True),
        uploader_frame=dict(size=(180, 135), crop='smart'),
    ),
}

###
# haystack должен быть подключен до своих приложений
#INSTALLED_APPS += ('haystack', )
HAYSTACK_INCLUDE_SPELLING = True
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_SITECONF = 'src.search.siteconf'
HAYSTACK_XAPIAN_PATH = os.path.join(PROJECT_DIR, 'search', 'xapian_index')
TEMPLATE_DIRS += (os.path.join(PROJECT_DIR, 'search', 'templates'), )

###
# modeltranslation
INSTALLED_APPS += ('modeltranslation', )
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'src.translation'

###
# markitup
INSTALLED_APPS += ('markitup', )
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})

###
# tagging-ng
INSTALLED_APPS += ('tagging', )
FORCE_LOWERCASE_TAGS = True
MAX_TAG_LENGTH = 255

try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass
