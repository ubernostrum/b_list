import os

import environ
import structlog


env = environ.Env(DEBUG=(bool, False))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Basic Django settings.
# ------------------------------------------------------------------------------

DEBUG = env("DEBUG")

DATABASES = {"default": env.db()}
DATABASES["default"]["CONN_MAX_AGE"] = 500

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "b_list.context_processors.current_site",
            ],
            "debug": DEBUG,
        },
    }
]

MIDDLEWARE = (
    "django_structlog.middlewares.RequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
)

CONTRIB_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.flatpages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_contact_form",
    "gunicorn",
    "typogrify",
    "widget_tweaks",
]

LOCAL_APPS = [
    "blog",
    "projects",
]

INSTALLED_APPS = CONTRIB_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "b_list.urls"
SECRET_KEY = env.str("SECRET_KEY")
WSGI_APPLICATION = "b_list.wsgi.application"


# Logging with structlog.
# ------------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "b_list": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


# Email.
# ------------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = "django@b-list.org"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")


# Static files.
# ------------------------------------------------------------------------------

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


# Security.
# ------------------------------------------------------------------------------

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG

SECURE_REFERRER_POLICY = "same-origin"

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_HOST = "www.b-list.org"
SECURE_SSL_REDIRECT = not DEBUG

X_FRAME_OPTIONS = "DENY"


# Content Security Policy, via django-csp.
# ------------------------------------------------------------------------------

CSP_SELF = "'self'"
CSP_DATA = "data:"
CSP_NONE = ["'none'"]

CSP_FONT_SRC = [CSP_SELF]
CSP_FORM_ACTION = [CSP_SELF]
CSP_IMG_SRC = [CSP_SELF, "https://github.com", CSP_DATA]
CSP_SCRIPT_SRC = [CSP_SELF]
CSP_STYLE_SRC = [CSP_SELF]
CSP_REQUIRE_SRI_FOR = ["script", "style"]

CSP_CONNECT_SRC = CSP_NONE
CSP_FRAME_ANCESTORS = CSP_NONE
CSP_FRAME_SRC = CSP_NONE
CSP_MEDIA_SRC = CSP_NONE
CSP_OBJECT_SRC = CSP_NONE
CSP_WORKER_SRC = CSP_NONE


# Miscellaneous settings.
# ------------------------------------------------------------------------------

ADMINS = (("James Bennett", env.str("MANAGER_EMAIL")),)
MANAGERS = ADMINS

LANGUAGE_CODE = "en-us"
USE_I18N = False
USE_L10N = False

TIME_ZONE = "America/Chicago"

SITE_ID = 1

MEDIA_URL = "http://media.b-list.org/m/"

PREPEND_WWW = not DEBUG
