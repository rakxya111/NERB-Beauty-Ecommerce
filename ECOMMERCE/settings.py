"""
Django settings for ECOMMERCE project.
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages

# -----------------------------------------
# BASE DIRECTORY
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------
# SECURITY SETTINGS
# -----------------------------------------
SECRET_KEY = 'django-insecure-gs#r5k=opvgl*a^yw7&@-5)49iju1mv384dglm_a!aj(c2so_-'

DEBUG = False  # 🚨 Turned OFF for deployment

# ✅ Add your PythonAnywhere domain here
ALLOWED_HOSTS = ['rakxya111.pythonanywhere.com', 'www.rakxya111.pythonanywhere.com']

# -----------------------------------------
# APPLICATIONS
# -----------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'mainshop',
    'accounts',
    'cart',
    'orders',
    'django_summernote',
]

# -----------------------------------------
# MIDDLEWARE
# -----------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware
    'cart.middleware.CartMiddleware',
]

# -----------------------------------------
# URLS & WSGI
# -----------------------------------------
ROOT_URLCONF = 'ECOMMERCE.urls'
WSGI_APPLICATION = 'ECOMMERCE.wsgi.application'

# -----------------------------------------
# TEMPLATES
# -----------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ ensure correct path type
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # custom context processors
                "mainshop.nav.navigation",
                "cart.nav.favourite_counter",
                'cart.context_processors.cart_item_count',
            ],
        },
    },
]

# -----------------------------------------
# DATABASE (SQLite)
# -----------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------------------
# STATIC & MEDIA FILES
# -----------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # ✅ where collectstatic will copy files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # ✅ absolute path for uploaded files

# -----------------------------------------
# AUTH & REDIRECTS
# -----------------------------------------
AUTH_USER_MODEL = 'accounts.Account'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -----------------------------------------
# MESSAGE TAGS
# -----------------------------------------
MESSAGE_TAGS = {
    messages.ERROR: "danger",
    50: "critical",
}

# -----------------------------------------
# SECURITY RECOMMENDATIONS (optional)
# -----------------------------------------
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
