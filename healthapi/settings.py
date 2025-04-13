from pathlib import Path
import os
import dj_database_url  # Added to parse the DATABASE_URL for deployment
from decouple import config  # Use python-decouple for better secrets handling
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'health-app-mvp.netlify.app',  # Your frontend URL on Netlify
    'https://health-tracker-gzw8.onrender.com',
    'localhost',                    # For local development
    '127.0.0.1',                    # Local development IP
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework',
    'django_extensions',
    'rest_framework_simplejwt',
    'health.apps.HealthConfig',
    'corsheaders',
    'whitenoise',  # Added Whitenoise for static files serving
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this for serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healthapi.urls'

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

WSGI_APPLICATION = 'healthapi.wsgi.application'


# Database
# Updated to use dj_database_url for production database
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL', cast=str, default='postgres://localhost/healthdb'))
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

# Serving static files in production
STATIC_URL = '/static/'  # URL to access static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collected static files

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Change default user model
AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Returns 10 results per page
}

CORS_ALLOWED_ORIGINS = [
    "https://health-app-mvp.netlify.app",  # Your production frontend
]


REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',  # Limit for logged-in users
        'rest_framework.throttling.AnonRateThrottle',  # Limit for guests
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/hour',  # Max 100 requests per hour for authenticated users
        'anon': '10/minute',  # Max 10 requests per minute for non-authenticated users
    }
})


# Default expiration times for tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Adjust access token lifetime as necessary
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Default refresh token lifetime
    'ROTATE_REFRESH_TOKENS': False,  # Set to True if you want to rotate refresh tokens
    'BLACKLIST_AFTER_ROTATION': False,
}
