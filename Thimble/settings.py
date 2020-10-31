"""
Django settings for Thimble project.

<<<<<<< HEAD
Generated by 'django-admin startproject' using Django 3.0.7.
=======
Generated by 'django-admin startproject' using Django 3.0.3.
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
<<<<<<< HEAD
SECRET_KEY = 'u9w_=i3v_1l4ntp%ijbc&npip)17mnpd@!+ju@r$7l@oi#dk(2'
=======
SECRET_KEY = os.environ['SECRET_KEY']
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

<<<<<<< HEAD
ALLOWED_HOSTS = ['138.197.214.125', 'localhost']
=======
ALLOWED_HOSTS = ['192.168.1.3', '192.168.1.11', 'thimbleapp.co', '138.197.214.125', 'localhost']

DATA_UPLOAD_MAX_MEMORY_SIZE = None
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
<<<<<<< HEAD
=======
    'rest_framework',
    'rest_framework.authtoken',
    'users.apps.UsersConfig',
    'notifications',
    'alerts.apps.AlertsConfig',
    'groups.apps.GroupsConfig',
    'posts.apps.PostsConfig',
    'likes.apps.LikesConfig',
    'django_mysql',
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Thimble.urls'

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

WSGI_APPLICATION = 'Thimble.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

<<<<<<< HEAD
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'thimbledb',
         'USER': 'doadmin',
         'PASSWORD': 'z5sps41j4f13zrla',
         'HOST': 'thimble-db-storage-do-user-8218478-0.b.db.ondigitalocean.com',
         'PORT': '25060',
         'OPTIONS': {
             "init_command": "SET foreign_key_checks = 0;",
             'charset': 'utf8mb4',
             'connect_timeout': 10,
         },
     }
}
=======
#Prod database
# if 'PROD_DB_PASSWORD' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'thimbledb',
            'USER': 'doadmin',
            'PASSWORD': os.environ['PROD_DB_PASSWORD'],
            'HOST': 'thimble-db-storage-do-user-8218478-0.b.db.ondigitalocean.com',
            'PORT': '25060',
            'OPTIONS': {
                "init_command": "SET foreign_key_checks = 0;",
                'charset': 'utf8mb4',
                'connect_timeout': 10,
            },
        }
    }

#Local database
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.environ['LOCAL_DB_NAME'],
#             'USER': 'root',
#             'PASSWORD': os.environ['LOCAL_DB_PASS'],
#             'HOST': 'localhost',
#             'PORT': '3306',
#             'OPTIONS': {
#                 "init_command": "SET foreign_key_checks = 0;",
#                 'charset': 'utf8mb4',
#                 'connect_timeout': 10,
#             },
#       }
# }
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

<<<<<<< HEAD
TIME_ZONE = 'UTC'
=======
TIME_ZONE = 'America/Los_Angeles'
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a

USE_I18N = True

USE_L10N = True

<<<<<<< HEAD
USE_TZ = True
=======
USE_TZ = False
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
<<<<<<< HEAD
=======

# Django rest framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}
>>>>>>> f299805e614a105e3bdde723d9e974d47467804a
