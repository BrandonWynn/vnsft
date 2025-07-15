"""
Django settings for your VNSFT project.
Production-ready with django-environ and .env support.
"""

import os
from pathlib import Path
import environ

# ✅ 1️⃣ Base directory — always your project root (same folder as manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ 2️⃣ Load env variables from .env in BASE_DIR
env = environ.Env(
    DEBUG=(bool, False)
)

# 💡 Explicit, bulletproof path — no guessing!
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# ✅ 3️⃣ Secret settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

AUTH_USER_MODEL = 'core.User'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.ngrok.io',
    '.ngrok-free.app',
    'vnsft.com',
    '.vnsft.com',
]

# ✅ 4️⃣ Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',   # If you use token auth
    'corsheaders',
    'core',                       # Replace with your actual app name!
]

# ✅ 5️⃣ Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'  # Change to your actual project folder if needed!

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'  # Match your project folder

# ✅ 6️⃣ Database — default SQLite, swap for Postgres later
DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')
}

# Example for Postgres later:
# DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME

# ✅ 7️⃣ Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ 8️⃣ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ 9️⃣ Static & media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ 🔗 CORS for React / React Native / Expo
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',   # Local React dev
    'https://vnsft.com',
]

# If you run Expo locally with changing IPs, loosen:
# CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'https://vnsft.com',
]

# ✅ 🔑 DRF auth for mobile token auth
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# ✅ 📋 Logging to console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ✅ Debug helper — optional
print(f"BASE_DIR: {BASE_DIR}")
print(f"SECRET_KEY exists: {'SECRET_KEY' in os.environ}")


