from .settings import *

ALLOWED_HOSTS = ['*']

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING['handlers'] = {
    'applogfile': {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': '/tmp/logs/app/app.log',
    },
}

LOGGING['loggers'] = {
    'django': {
        'handlers': ['applogfile'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
}

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
