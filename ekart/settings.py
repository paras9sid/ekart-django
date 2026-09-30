
import environ
import os

from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config # for env file creation - second method after environ


env = environ.Env()

environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY=env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# if using decouple - and config
# DEBUG = env('DEBUG', default=True, cast=bool) # True - default value if nothing inside debug key

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['djangoekart.in','ekart-django-production.up.railway.app', '*']

CSRF_TRUSTED_ORIGINS = ['https://www.djangoekart.in','https://ekart-django-production.up.railway.app']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "category",
    "accounts",
    "store",
    "carts",
    "orders",
    "admin_honeypot",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
]

ROOT_URLCONF = "ekart.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "category.context_processors.menu_links",
                "carts.context_processors.counter",
                "ekart.context_processors.paypal_client_id"
            ],
        },
    },
]

WSGI_APPLICATION = "ekart.wsgi.application"

#using custom user model - notifying settings.py
AUTH_USER_MODEL = 'accounts.Account' # appName(accounts).modelName(Account)


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': env('DB_NAME'),

        'USER': env('DB_USER'),

        'PASSWORD': env('DB_PASSWORD'),

        'HOST': env('DB_HOST'),

        'PORT': env('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"

#"Indian TimeZone"
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR /'staticfiles'

# STATICFILES_DIRS = [
#     'ekart/static',
# ]

# Railway bucket - 

AWS_ACCESS_KEY_ID = env('ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('BUCKET_NAME') 
AWS_S3_ENDPOINT_URL = env('ENDPOINT_URL')
AWS_S3_REGION_NAME = env('REGION')

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # MEDIA FILES

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR /'media'


MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


# SMTP configuration

#only for checking link not from gmail from inbuilt django
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

##
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# paypal button pop up error- solution - error in console - popup_open_error_iframe_fallback 
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

#PAYPAL
PAYPAL_CLIENT_ID=env('PAYPAL_CLIENT_ID')

#RAZORPAY
RZP_KEY_ID=env('RZP_KEY_ID')
RZP_KEY_SECRET=env('RZP_KEY_SECRET')




#Session timeout - automatic logout from admin.
# SESSION_EXPIRE_SECONDS = 3600  # 1 hour = 3600 seconds

SESSION_EXPIRE_SECONDS = 300 # 60 seconds = 1 minutes of no activity
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = 'accounts/login'

# for indian pricing of products

LANGUAGE_CODE = 'en-in' 

USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
