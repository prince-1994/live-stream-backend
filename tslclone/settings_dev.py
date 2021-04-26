from .settings_base import *
import os

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

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl' : 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'media'

DEFAULT_FILE_STORAGE = 'tslclone.storages.MediaStore'
