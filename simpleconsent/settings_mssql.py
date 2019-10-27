# this file contains secret keys. Protect file or insert values from environment

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '66_!!m)!ks&v)2cjy)m6+uhtm%0jz7*1+tu@whlebrqsb@b##z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost', 'wpvconsent.vnet', 'consent.wko.at', 'consent.qss.wko.at']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
#    }
#}

# Setting for django-mssql-backend
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'simpleconsent',
        'HOST': '192.168.0.37',
        'PORT': '1433',
        'USER': 'SA',
        'PASSWORD': 'scott',
        'OPTIONS': {
            'host_is_server': True,
            #'driver': 'FreeTDS',
            'driver': 'ODBC Driver 13 for SQL Server',
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'de-AT'
TIME_ZONE = 'Europe/Vienna'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Authentication for API user that writes consent records
BASICAUTH_USERS = {'admin': 'adminadmin'}  # TODO: change weak default password
BASICAUTH_REALM: 'api_user'
# shared secret: configure same ASCII-value in proxy and consent app
PROXY_HMAC_KEY = b'leMn00UscEDWEtt/vvHs0v/+Wqjxih/WxixZOMLt'
# redirect to URL after the use accepted or declined consent
PROXY_HANDLE_CONSENT_RESPONSE_URL = 'https://satosa.vnet/simpleconsent_response'
CONSENT_BOILERPLATE_TEXT = {
    'purpose': 'Der Zweck der Datenweitergabe ist die Identifikation am ausgewählten Service. '
               'Wird keine Einwilligung gegeben, kann das Service, an das die Anmeldedaten übermittelt werden, '
               'möglicherweise die Anmeldung ablehnen.',
    'revocation': 'Die Einwilligung kann jederzeit widerrufen werden. '
                  'Bitte kontaktieren Sie dazu das Support Team der WKO Inhouse unter QuS@inhouse.wko.at '
                  'und der Angabe Ihres Namens und Ihrer Benutzerkennung. '
                  'Wird die Einwilligun widerrufen, erfolgt beim nächsten Login die Abfrage der Einwilligung.',
    'title': 'Attributfreigabe für die Anmeldung an',
}


# ====== The configuration below should not be changed in regular deployments ======


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'consent',
    #'mysql_test',
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

ROOT_URLCONF = 'simpleconsent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'simpleconsent.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
