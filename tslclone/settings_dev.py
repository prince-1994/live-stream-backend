from .settings_base import *
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('AWS_RDS_POSTGRES_DB_NAME'),
        'USER': os.environ.get('AWS_RDS_POSTGRES_USER'),
        'PASSWORD': os.environ.get('AWS_RDS_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('AWS_RDS_POSTGRES_HOST'),
        'PORT': os.environ.get('AWS_RDS_POSTGRES_PORT'),
    }
}

CHANNEL_LAYERS = {
    'default' : {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts' : [('127.0.0.1', 6379)],
        }
    }
}

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl' : 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'media'

DEFAULT_FILE_STORAGE = 'tslclone.storages.MediaStore'

SENTRY_DSN = os.environ.get('SENTRY_DSN')

sentry_sdk.init(
    dsn=os.environ.get(SENTRY_DSN),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)