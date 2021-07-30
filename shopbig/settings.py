from pathlib import Path
import os
import logging
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# ENV
ENV = os.environ.get("ENV")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "channels",
    "django_filters",
    "taggit",
    "taggit_serializer",
    "imagekit",
    # local
    "apps.users.apps.UsersConfig",
    "apps.channels.apps.ChannelsConfig",
    "apps.products.apps.ProductsConfig",
    "apps.shows.apps.ShowsConfig",
    "apps.chats.apps.ChatsConfig",
    "apps.checkout.apps.CheckoutConfig",
    "apps.profiles.apps.ProfilesConfig",
    "apps.payout.apps.PayoutConfig",
    "apps.images.apps.ImagesConfig",
]

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shopbig.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Rest Framework
# https://www.django-rest-framework.org/
DJANGO_REST_PAGE_SIZE = os.environ.get("DJANGO_REST_PAGE_SIZE", 15)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": DJANGO_REST_PAGE_SIZE,
}

# Djoser Framework
DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": os.environ.get("DJANGO_PASSWORD_RESET_URL"),
    "ACTIVATION_URL": os.environ.get("DJANGO_ACTIVATION_URL"),
    "USER_CREATE_PASSWORD_RETYPE": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SERIALIZERS": {
        "user": "apps.users.serializers.UserSerializer",
        "current_user": "apps.users.serializers.UserSerializer",
    },
    # 'EMAIL': {
    #     'activation': 'users.email.ActivationEmail',
    #     'confirmation': 'users.email.ConfirmationEmail',
    #     'password_reset': 'users.email.PasswordResetEmail',
    #     'password_changed_confirmation': 'users.email.PasswordChangedConfirmationEmail',
    # }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = ".media/"


# Logging
DJANGO_LOGGING = os.environ.get("DJANGO_LOGGING")
if DJANGO_LOGGING:
    LOGGING = {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
            },
        },
        "root": {
            "handlers": ["console"],
        },
    }


# Auth User Model
AUTH_USER_MODEL = "ShopbigUsers.User"

# Auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django
DOMAIN = os.environ.get("DJANGO_DOMAIN", "shopbig.live")
SITE_NAME = os.environ.get("DJANGO_SITE_NAME", "ShopBigLive")


# AWS IVS
AWS_IVS_ACCESS_KEY = os.environ.get("AWS_IVS_ACCESS_KEY", "")
AWS_IVS_SECRET_KEY = os.environ.get("AWS_IVS_SECRET_KEY", "")
AWS_IVS_RECORDING_CONFIGURATION_ARN = os.environ.get(
    "AWS_IVS_RECORDING_CONFIGURATION_ARN"
)
AWS_IVS_CHANNEL_TYPE = os.environ.get("AWS_IVS_CHANNEL_TYPE")
AWS_IVS_VIDEO_CDN = os.environ.get("AWS_IVS_VIDEO_CDN")


# AWS S3
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_DEFAULT_ACL = "public-read"
AWS_LOCATION = os.environ.get("AWS_LOCATION","")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")

# Email
EMAIL_BACKEND_TYPE = os.environ.get("EMAIL_BACKEND_TYPE")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL")
EMAIL_BACKEND = f"django.core.mail.backends.{EMAIL_BACKEND_TYPE}.EmailBackend"


# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_ORDERS_ENDPOINT_SECRET = os.environ.get("STRIPE_ORDERS_ENDPOINT_SECRET")


# Taggit
TAGGIT_CASE_INSENSITIVE = True


# Imagekit
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"


# Databases
DB_ENGINE_TYPE = os.environ.get("DB_ENGINE_TYPE", "")
DB_NAME = os.environ.get("DB_NAME", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "")
DB_PORT = os.environ.get("DB_PORT", "")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends." + DB_ENGINE_TYPE,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# Channel layers
DJANGO_REDIS_CHANNEL_LAYERS_HOSTS_STRING = os.environ.get(
    "DJANGO_REDIS_CHANNEL_LAYERS_HOSTS", ""
)
if DJANGO_REDIS_CHANNEL_LAYERS_HOSTS_STRING:
    DJANGO_REDIS_CHANNEL_LAYERS_HOSTS = list(
        map(
            lambda x: x.split(":"),
            os.environ.get("DJANGO_REDIS_CHANNEL_LAYERS_HOSTS", "").split(","),
        )
    )
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": DJANGO_REDIS_CHANNEL_LAYERS_HOSTS,
            },
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }

# Django Application
WSGI_APPLICATION = "shopbig.wsgi.application"
ASGI_APPLICATION = "shopbig.asgi.application"


# File storage
if not ENV in ["local"]:
    DEFAULT_FILE_STORAGE = "shopbig.storages.MediaStore"

# SENTRY
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=os.environ.get(SENTRY_DSN),
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
