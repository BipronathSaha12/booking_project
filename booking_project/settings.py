import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'your-secret-key'
DEBUG = True
# For local development, allow localhost and common dev hosts.
# In production, set this to your real domain(s).
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
ALLOWED_HOSTS = ["*"] 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'booking_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],},
    },
]

WSGI_APPLICATION = 'booking_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR/'staticfiles'

# bookings app lives one level above BASE_DIR (which is the folder containing manage.py),
# so include its static/ directory explicitly.
STATICFILES_DIRS = [BASE_DIR.parent / 'bookings' / 'static']

# Note: WhiteNoise is already enabled in the MIDDLEWARE list above.

# Media Files (Service Images, QR Codes)

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Stripe
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bipronathsaha@gmail.com'
EMAIL_HOST_PASSWORD = 'kiyk rmvm jfux gwbf'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
