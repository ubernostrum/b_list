import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Basic Django settings.
# ------------------------------------------------------------------------------

DEBUG = bool(int(os.getenv('DJANGO_DEBUG', 0)))

DATABASES = {}
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['CONN_MAX_AGE'] = 500


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        }
    }
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'csp.middleware.CSPMiddleware',    
    'django.middleware.gzip.GZipMiddleware',
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
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'blog',
    'contact_form',
    'typogrify',
    'gunicorn',
    'projects',
    'widget_tweaks',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
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
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['*']


# Email.
# ------------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = 'django@b-list.org'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']


# Static files.
# ------------------------------------------------------------------------------

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


# Security.
# ------------------------------------------------------------------------------

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_HOST = 'www.b-list.org'
SECURE_SSL_REDIRECT = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True


# CSP.
# ------------------------------------------------------------------------------

CSP_SELF = "'self'"
CSP_NONE = ["'none'"]

CSP_FONT_SRC = [CSP_SELF, 'https://fonts.gstatic.com']
CSP_FORM_ACTION = [CSP_SELF]
CSP_IMG_SRC = [CSP_SELF]
CSP_SCRIPT_SRC = [CSP_SELF, 'https://code.jquery.com']
CSP_STYLE_SRC = [CSP_SELF, 'https://fonts.googleapis.com']
CSP_REQUIRE_SRI_FOR = ['script', 'style']

CSP_CHILD_SRC = CSP_NONE
CSP_CONNECT_SRC = CSP_NONE
CSP_FRAME_ANCESTORS = CSP_NONE
CSP_FRAME_SRC = CSP_NONE
CSP_MEDIA_SRC = CSP_NONE
CSP_OBJECT_SRC = CSP_NONE


# Miscellaneous settings.
# ------------------------------------------------------------------------------

ADMINS = (
    ('James Bennett', os.environ['MANAGER_EMAIL']),
)
MANAGERS = ADMINS
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = False
USE_L10N = False
SITE_ID = 1
MEDIA_URL = 'http://media.b-list.org/m/'
PREPEND_WWW = not DEBUG

