"""
Django settings for memprot_project project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&u0=z#6!8@44@kgm3ce$bu2+wt^1%y!(ljsrnn6gqqwxz9lu4g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ('127.0.0.1', 'localhost',
                 '192.168.157.149', '192.168.157.149.')


#CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cnelson.django.test@gmail.com'
EMAIL_HOST_PASSWORD = 'Lazenby0'
EMAIL_PORT = 465
EMAIL_USE_SSL = True


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webform',
    #'djcelery',
    'social_django',
    'django_rq',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    )

ROOT_URLCONF = 'memprot_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'memprot_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# password hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (STATIC_DIR, )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Authentication methods provided by python-social-auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.github.GithubOAuth2',
    'social.backends.zotero.ZoteroOAuth',
    'social.backends.google.GoogleOAuth2',
)
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_USER_MODEL = 'webform.UserProfile'

SOCIAL_AUTH_GITHUB_KEY = 'c1f8df1469375db82e49'
SOCIAL_AUTH_GITHUB_SECRET = 'e9bcf59efaa6a6990abf654852f504dd8449cfe4'

SOCIAL_AUTH_ZOTERO_KEY = '0f40744a282798ee1346'
SOCIAL_AUTH_ZOTERO_SECRET = '136241b902bd6399adfd'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '879494813518-rcbi4hintm2ae2kgocleab9dd7b1b720.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '_g-lvlvnivjx-AgJ3s8PgGV5'


# Redis Queues

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}





