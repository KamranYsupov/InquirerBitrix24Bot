import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from pyrogram.enums import ParseMode

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Библиотеки
    'django_extensions',
    
    # Приложения
    'web.apps.bitrix24',
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

ROOT_URLCONF = 'web.core.urls'

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

WSGI_APPLICATION = 'web.core.wsgi.application'
ASGI_APPLICATION = 'web.core.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = ['https://kamran.loca.lt']

BITRIX24_WEBHOOK_APPLICATION_TOKEN = os.getenv('BITRIX24_WEBHOOK_APPLICATION_TOKEN')
BITRIX24_API_URL = os.getenv('BITRIX24_API_URL')
BITRIX24_TELEGRAM_USERNAME_FIELD_NAME = os.getenv('BITRIX24_TELEGRAM_USERNAME_FIELD_NAME')
BITRIX_CRM_DEAL_URL = 'https://avgrup.bitrix24.ru/crm/deal/details/{0}/'

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Настройки юзербота
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
USERBOT_PHONE = os.getenv('USERBOT_PHONE')
USERBOT_LOGIN = os.getenv('USERBOT_LOGIN')
USERBOT_DATA = {
    'name': USERBOT_LOGIN,
    'api_id': TELEGRAM_API_ID,
    'api_hash': TELEGRAM_API_HASH,
    'phone_number': USERBOT_PHONE,
    'parse_mode': ParseMode.HTML,
    'workdir': str(BASE_DIR),
}


MANAGERS_GROUP_ID = int(os.getenv('MANAGERS_GROUP_ID'))

TELEGRAM_API_URL = 'https://api.telegram.org'
