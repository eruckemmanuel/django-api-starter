"""
Django settings for app project.
"""
from pathlib import Path
import os
import time
from uuid import uuid4
from django.utils import timezone
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from corsheaders.defaults import default_headers

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='NO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'channels',
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'oauth2_provider',
    'cid.apps.CidAppConfig'
]

# Custom apps
CUSTOM_APPS = [
    'common',
    'account',
]

# Combine custom apps with installed apps
INSTALLED_APPS += CUSTOM_APPS

# AUTH MODEL
AUTH_USER_MODEL = 'account.User'

MIDDLEWARE = [
    # Correlation ID middleware
    'cid.middleware.CidMiddleware',
    # 'request_logging.middleware.LoggingMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS Middleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cid.context_processors.cid_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

ASGI_APPLICATION = "app.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASE_ENGINES = {
    "postgresql": 'cid.backends.postgresql',
    "mysql": 'cid.backends.mysql',
    "oracle": 'cid.backends.oracle'
}

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINES.get(config('DB_ENGINE', default="postgresql")),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'oauth2_provider.contrib.rest_framework.permissions.TokenHasReadWriteScope',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redis Channel configs
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + []

# Correlation ID settings
CID_GENERATE = True
CID_CONCATENATE_IDS = True
CID_GENERATOR = lambda: f'{time.time()}-{str(uuid4())}'
CID_HEADER = 'HTTP_X_CORRELATION_ID'
CID_RESPONSE_HEADER = 'X-Correlation-Id'

# LOGGING
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[cid: %(cid)s] %(levelname)s %(asctime)s %(request)s %(module)s  %(message)s'
        },
        'db_backend': {
            'format': '[cid: %(cid)s] %(levelname)s %(asctime)s %(duration)s %(sql)s, %(params)s %(module)s  %(message)s'
        },
        'request_format': {
            '()': 'common.utils.log.RequestLogFormatter',
            'format': '[APP_ID: %(app_id)s] [cid: %(cid)s] %(levelname)s %(asctime)s %(http_method)s %(username)s %(headers)s %(module)s  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'request_format',
            'filters': ['correlation', 'request'],
        },
        'file': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.FileHandler',
            'filename': config('LOG_FILE', 'general.log'),
            'formatter': 'verbose',
            'filters': ['correlation'],
        },

    },
    'filters': {
        'correlation': {
            '()': 'cid.log.CidContextFilter'
        },
        'request': {
            '()': 'django_requestlogging.logging_filters.RequestFilter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'filters': ['correlation', 'request'],
            'propagate': False,
            'level': 'INFO'
        },
        'django.db.backends': {
            'handlers': ['console'],
            'filters': ['correlation'],
            'formatter': 'db_backend',
            'propagate': True
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'filters': ['correlation', 'request'],
        'formatter': 'request_format',
    },
}

# Sentry
ENABLE_SENTRY_LOG = config('ENABLE_SENTRY_LOG', default=False, cast=bool)
if ENABLE_SENTRY_LOG:
    sentry_sdk.init(
        dsn=config('SENTRY_DSN', default=""),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

# Graylog
ENABLE_GRAYLOG = config('ENABLE_GRAYLOG', default=False, cast=bool)
if ENABLE_GRAYLOG:
    LOGGING['handlers']['graylog'] = {
        'level': 'DEBUG',
        'class': 'graypy.GELFHTTPHandler',
        'host': config('GRAYLOG_SERVER_HOST', default='localhost'),
        'port': config('GRAYLOG_SERVER_PORT', default=12201),
        'formatter': 'request_format'
    }
    LOGGING['root']['handlers'].append('graylog')
    LOGGING['loggers']['django']['handlers'].append('graylog')

# OIDC

OAUTH2_PROVIDER = {
    "OIDC_ENABLED": config('OIDC_ENABLED', default=True, cast=bool),
    "OIDC_RSA_PRIVATE_KEY": config("OIDC_RSA_PRIVATE_KEY", default='NOT_SECURE_KEY'),
    "SCOPES": {
        "openid": "OpenID Connect scope",
    },
}
