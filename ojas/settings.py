import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'a_super_secret_key'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rest_framework',
    'blog',
    'taggit',
    'embed_video',
    'ckeditor',
    'user_visit',
    'django_user_agents',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'ojas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'blog/templates')],
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


WSGI_APPLICATION = 'ojas.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 1
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
    },
}

SERVER_EMAIL = '******@gmail.com'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = '****'
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = [('****', '****@gmail.com'), ]

LOGO_URL = 'https://github.com/ahampriyanshu/ojas/raw/main/static/img/logo.png'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '{name} {levelname} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{asctime} {name} {levelname} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'blog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': 'logs/blog.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['console'],
        },
        'blog.views': {
            'level': 'DEBUG',
            'handlers': ['console', 'blog'],
            'propagate': False,
        },
        'django.security': {
            'level': 'CRITICAL',
            'handlers': ['mail_admins', ],
            'propagate': False,
        },
    }
}
