import os

from django.conf import settings
from dotenv import load_dotenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
#   EC2 Public IPV4 DNS
    "ec2-3-95-23-176.compute-1.amazonaws.com",
#   Custom Domain Name
    "ruffinweb.com"
    "ruffinweb.com/api",
]


# Application definition

INSTALLED_APPS = [
    "backend.apps.BackendConfig",
    "rest_framework",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        # "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:80",  # for SSL, forwarded to 400
    "http://localhost:8000",  # development backend server
    "http://localhost:3000",  # development frontend server
    # these should be the final settings
    "https://ruffinweb.com",  # cloudfront distribution custom domain name.
    # "https://backend-server-domain.com",
    # "http://cloudfront-domain.s3.amazonaws.com",
]

CSRF_TRUSTED_ORIGIN = [
    "http://localhost:80",  # for SSL, forwarded to 400
    "http://localhost:8000",  # development backend server
    "http://localhost:3000",  # development frontend server
    # these should be the final settings
    "https://ruffinweb.com",  # cloudfront distribution custom domain name.
    # "https://backend-server-domain.com",
    # "http://cloudfront-domain.s3.amazonaws.com",
]


ROOT_URLCONF = "RuffinwebProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "RuffinwebProject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PG_DATABASE_NAME"),
        "USER": os.getenv("PG_USER"),
        "PASSWORD": os.getenv("PG_PASSWORD"),
        "HOST": os.getenv("EMAIL_USER"),
        "PORT": os.getenv("PG_PORT"),
        "CLIENT_ENCODING": "UTF8",
        "DEFAULT_TRANSACTION_ISOLATION": "read committed",
        "TIMEZONE": "UTC"
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Most static files will be stored in an S3 bucket.
# The index and error pages are all stored with the frontend.
# The only file in the stored with the backend is the email reply page.
# STATIC_ROOT = "s3://bucket-name/static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    # BASE_DIR / "static",
    # "/var/www/static/",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Add logging

env_file_s = os.getenv("EMAIL_USER")
database_s = DATABASES
cors_s = CORS_ALLOWED_ORIGINS


def export_settings():
  settings_object = [env_file_s, database_s, cors_s]
  print(settings_object)
# return settings_object
