import os

import dj_database_url


DEBUG = False
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': dj_database_url.config(),
}

DATABASES['default']['ENGINE'] = 'django_postgrespool'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'flat',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django_browserid',
    'blog',
    'contact_form',
    'typogrify',
    'gunicorn',
    'projects',
)

AUTHENTICATION_BACKENDS = (
    'django_browserid.auth.BrowserIDBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ROOT_URLCONF = 'b_list.urls'

WSGI_APPLICATION = 'b_list.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

ADMINS = (
    ('James Bennett', 'james@b-list.org'),
)

DEFAULT_FROM_EMAIL = 'django@b-list.org'

MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
TIME_ZONE = 'America/Chicago'
USE_I18N = False
USE_L10N = False

STATIC_URL = 'http://media.b-list.org/'
MEDIA_URL = 'http://media.b-list.org/m/'

# Required by django-browserid.
SITE_URL = 'http://www.b-list.org'
LOGIN_REDIRECT_URL = '/'
BROWSERID_CREATE_USER = False
