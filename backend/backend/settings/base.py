"""
Django settings for learn project.

Generated by 'django-admin startproject' using Django 5.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
import os


# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environment variables
env = environ.Env()

# Take environment variables from .env file
env_file = os.path.join(os.path.join(BASE_DIR, "./"), '.env')
env.read_env(env_file)

# print(50 * "*")
# print(BASE_DIR)
# print(env_file)
# print(env)
# print(50 * "*")

# Debugging prints to check the loaded environment variables
# print(50 * "*")
# print(env('POSTGRES_DB'))  # Example to check if DEBUG is loaded
# print(env('POSTGRES_USER'))  # Example to check if SECRET_KEY is loaded
# print(50 * "*")

# Function to read secrets (e.g., from Docker secrets)
def read_secret(secret_name):
    try:
        with open(secret_name) as f:
            return f.read().strip()
    except IOError:
        return None


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(-oe#et7h*sb9d@e70y-gm7h#qnoe0-(&b)^l9%!b=6f7k^x7&'

# Application definition

INSTALLED_APPS = [
    'menu.apps.MenuConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_htmx",
    'authentication.apps.AuthenticationConfig',
    'django.contrib.postgres',
]

AUTHENTICATION_BACKENDS = [
    'authentication.backends.CustomBackend',  # Custom backend goes here
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, './menu/templates'),
                 os.path.join(BASE_DIR, './authentication/templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': read_secret(env('POSTGRES_PASSWORD_FILE')),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, '../var/www/example.com/static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, './static'),
    os.path.join(BASE_DIR, './menu/static'),
    os.path.join(BASE_DIR, './authentication/static'),
]


# Media files
MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, '../var/www/example.com/media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom menu user
AUTH_USER_MODEL = "authentication.User"


# Redirection URLs
LOGIN_REDIRECT_URL = 'menu:dashboard'
LOGOUT_REDIRECT_URL = '/authentication/login'
LOGIN_URL = 'authentication:login'
LOGOUT_URL = 'authentication:logout'

