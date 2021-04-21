from .settings_base import *

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
