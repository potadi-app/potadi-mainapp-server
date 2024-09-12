import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    
    'rest_framework',
    'rest_framework.authtoken',
    
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    'dj_rest_auth',
    
    'drf_yasg',
    
    'accounts',
    'diagnose',
    
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # allauth middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Digital Assets Management
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}


# Custom user model
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Django REST Auth
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserDetailsSerializer',
    'REGISTER_SERIALIZER': 'accounts.serializers.RegisterSerializer',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Sesi login 15 menit untuk access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh token berlaku selama 7 hari
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SITE_ID = 1  # Pastikan kamu telah menetapkan Site ID yang benar

ACCOUNT_AUTHENTICATION_METHOD = "email"  # Use Email / Password authentication
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none" # Do not require email confirmation

# Authenticate if local account with this email address already exists
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
# Connect local account and social account if local account with that email address already exists
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
            },
        'SCOPE': [
            'profile',
            'email',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
            "prompt": "consent",
        },
        'FETCH_USER_INFO': True,
        'OAUTH_PKCE_ENABLED': True,
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

CORS_ORIGIN_ALLOW_ALL = True

GOOGLE_OAUTH_CALLBACK_URL = os.getenv('GOOGLE_OAUTH_CALLBACK_URL')
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

CSRF_COOKIE_HTTPONLY = True