from pathlib import Path
import os
from channels.apps import ChannelsConfig
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(':')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'channels',

    # local
    "apps.users.apps.UsersConfig",
    "apps.channels.apps.ChannelsConfig",
    "apps.products.apps.ProductsConfig",
    "apps.shows.apps.ShowsConfig",
    "apps.chats.apps.ChatsConfig",
    "apps.checkout.apps.CheckoutConfig",
    "apps.profiles.apps.ProfilesConfig",
    "apps.payout.apps.PayoutConfig",
    "apps.applications.apps.ApplicationsConfig",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tslclone.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'tslclone.wsgi.application'

# Rest Framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

# Djoser Framework
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': os.environ.get('DJANGO_PASSWORD_RESET_URL'),
    'ACTIVATION_URL': os.environ.get('DJANGO_ACTIVATION_URL'),
    'SEND_ACTIVATION_EMAIL': True,
    "SEND_CONFIRMATION_EMAIL": True,
    'SERIALIZERS': {
        'user': 'apps.users.serializers.UserSerializer',
        'current_user': 'apps.users.serializers.UserSerializer',
    },

    # 'EMAIL': {
    #     'activation': 'users.email.ActivationEmail',
    #     'confirmation': 'users.email.ConfirmationEmail',
    #     'password_reset': 'users.email.PasswordResetEmail',
    #     'password_changed_confirmation': 'users.email.PasswordChangedConfirmationEmail',
    # }
}

CORS_ORIGIN_ALLOW_ALL = True

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# # Logging
# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#     }
# }

MEDIA_URL = "/media/"

MEDIA_ROOT = ".media/"

AUTH_USER_MODEL = 'TslCloneUsers.User'

DOMAIN = os.environ.get('VUE_FRONTEND_HOST')
SITE_NAME = os.environ.get('DJANGO_SITE_NAME')
# EMAIL_BACKEND = 'django_ses.SESBackend'

# AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION')
# AWS_SES_REGION_ENDPOINT = os.environ.get('AWS_SES_HOST')

AWS_S3_RECORDING_CONFIGURATION = os.environ.get('AWS_S3_RECORDING_CONFIGURATION')
AWS_IVS_VIDEO_CDN = os.environ.get('AWS_IVS_VIDEO_CDN')

EMAIL_PORT = os.environ.get('AWS_SES_PORT')
EMAIL_HOST = os.environ.get('AWS_SES_HOST')
EMAIL_HOST_USER = os.environ.get('AWS_SES_ACCESS_KEY_ID')
EMAIL_HOST_PASSWORD = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL')

ASGI_APPLICATION = 'tslclone.asgi.application'

CHANNEL_LAYERS = {
    'default' : {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts' : [('127.0.0.1', 6379)],
        }
    }
}

STRIPE_PUBLISHABLE_KEY=os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY=os.environ.get('STRIPE_SECRET_KEY')
STRIPE_ORDERS_ENDPOINT_SECRET=os.environ.get('STRIPE_ORDERS_ENDPOINT_SECRET')

ENV=os.environ.get('ENV')