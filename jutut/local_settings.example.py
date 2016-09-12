#DEBUG = True
#SECRET_KEY = '' # will be autogenerated in secret_key.py if not specified here
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
#ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        # use ident auth for local servers
        # and add passwd&hostname etc for remote
    }
}

#CACHES = {
#    'default': {
#        # prefer memcached with unix socket
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': 'unix:/tmp/memcached.sock',
#
#        # Database cache, if memcached is not possible
#        # remember to run `./manage.py createcachetable`
#        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#        'LOCATION': 'django_cache_default',
#
#        # For development local memory
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#        'LOCATION': 'unique-snowflake',
#        # or dummy
#        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#    }
#}

# For debugging purposes
#from .settings import LOGGING
#LOGGING['loggers'] = {
#    '': {
#        'level': 'INFO',
#        'handlers': ['debug_console'],
#        'propagate': True,
#    },
#    'aplus_client.client': {
#        'level': 'DEBUG',
#    },
#    'django.db.backends': {
#        'level': 'DEBUG',
#    },
#}
