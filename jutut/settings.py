"""
Django settings

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os, warnings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.utils.translation import ugettext_lazy as _

# Base options, commonly overridden in local_settings.py
###############################################################################
DEBUG = False
SECRET_KEY = None
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
#SERVER_EMAIL = 'root@'
ALLOWED_HOSTS = ["*"]


# Jutut options (do not effect django framework)
###############################################################################
# Automatically accept with best grade feedbacks that do not have any required
# text fields and no answer in option text fields
JUTUT_AUTOACCEPT_ON = True
# minimum length in text field to count it as filled
JUTUT_TEXT_FIELD_MIN_LENGTH = 2
# Show only best grade for feedbacks that do not contain any required text fields
JUTUT_OBLY_ACCEPT_ON = True


# Content (may override in local_settings.py)
#
# Any templates can be overridden by copying into
# local_templates/possible_path/template_name.html
###############################################################################

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # 3rd party libs
    'bootstrapform',
    # libs
    'django_lti_login',
    'django_colortag',
    'aplus_client',
    'dynamic_forms',
    'django_dictiterators',
    # project apps
    'accounts',
    'feedback',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django_lti_login.backends.LTIAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'local_templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

ROOT_URLCONF = 'jutut.urls'
WSGI_APPLICATION = 'jutut.wsgi.application'
LOGIN_REDIRECT_URL = '/manage/'


# Database (override in local_settings.py)
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mooc_jutut_prod',
        #'USER': 'username',
        #'PASSWORD': 'mypassword',
        #'HOST': '127.0.0.1',
        #'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'accounts.JututUser'
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


# LTI login parameters: our site allows only course staff to enter using lti login
LTI_ACCEPTED_ROLES = ('Instructor', 'TeachingAssistant')
LTI_STAFF_ROLES = ('Instructor')


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'EET'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fi', _('Finnish')),
    ('en', _('English')),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Cache
# https://docs.djangoproject.com/en/1.9/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}


# Logging
# https://docs.djangoproject.com/en/1.7/topics/logging/
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'verbose': {
      'format': '[%(asctime)s: %(levelname)s/%(module)s] %(message)s'
    },
    'colored': {
      '()': 'lib.logging.SourceColorizeFormatter',
      'format': '[%(asctime)s: %(levelname)8s %(name)s] %(message)s',
      'colors': {
        'aplus_client.client': {'fg': 'red', 'opts': ('bold',)},
        'django.db.backends': {'fg': 'cyan'},
      },
    },
  },
  'filters': {
    'require_debug_true': {
      '()': 'django.utils.log.RequireDebugTrue',
    }
  },
  'handlers': {
    'debug_console': {
      'level': 'DEBUG',
      'filters': ['require_debug_true'],
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',
      'formatter': 'colored',
    },
    'console': {
      'level': 'INFO',
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',
      'formatter': 'verbose',
    },
    'mail': {
      'level': 'ERROR',
      'class': 'django.utils.log.AdminEmailHandler',
    },
  },
  'loggers': {
    '': {
      'level': 'INFO',
      'handlers': ['console'],
      'propagate': True
    },
    'requests': { 'level': 'WARNING' },
  },
}


# Django fitlers
# https://django-filter.readthedocs.io/en/latest/ref/settings.html
FILTERS_HELP_TEXT_EXCLUDE = False
FILTERS_HELP_TEXT_FILTER = False


###############################################################################
#
# Settings logic to handle local settings and any reactions to them
#

# Overrides and appends settings defined in local_settings.py
try:
    from local_settings import *
except ImportError:
    try:
        from jutut.local_settings import *
    except ImportError:
        # make a warning that there is no local_settings, but ignore the exception
        warnings.warn("Couldn't find local_settings.py from project root nor under aplus/")
        pass

if not SECRET_KEY:
    try:
        from .secret_key import SECRET_KEY
    except ImportError:
        from lib.helpers import create_secret_key_file
        settings_dir = os.path.abspath(os.path.dirname(__file__))
        key_filename = os.path.join(settings_dir, 'secret_key.py')
        create_secret_key_file(key_filename)
        warnings.warn("SECRET_KEY not defined in local_settings.py, created one in %s" % (key_filename,))
        del settings_dir
        del create_secret_key_file
        del key_filename
        from .secret_key import SECRET_KEY

if not DEBUG:
    # when not in debug mode, add cached loader on top of template loaders
    cached_loader = 'django.template.loaders.cached.Loader'
    for backend in TEMPLATES:
        options = backend.get('OPTIONS')
        loaders = options and options.get('loaders')
        if loaders and cached_loader not in loaders:
            loaders = ((cached_loader, loaders),)
            backend['OPTIONS']['loaders'] = loaders
