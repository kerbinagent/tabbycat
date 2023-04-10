ON_LOCAL = True

# ==============================================================================
# Settings that you should specify
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE'      : 'django.db.backends.postgresql',
        'NAME'        : 'tournament',  # put your PostgreSQL database's name in here
        'USER'        : 'tabroom',  # put your PostgreSQL login role's user name in here
        'PASSWORD'    : 'tab123',  # put your PostgreSQL login role's password in here
        'HOST'        : 'localhost',
        'PORT'        : '5432',
        'CONN_MAX_AGE': None,
    }
}

# Replace this with your time zone, as defined in the IANA time zone database:
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
TIME_ZONE = 'Asia/Singapore'

# ==============================================================================
# Overwrites main settings
# ==============================================================================

ADMINS              = ()
MANAGERS            = ADMINS
DEBUG               = True
DEBUG_ASSETS        = True
# SECRET_KEY          = ""

# ==============================================================================
# Redis
# ==============================================================================

USE_REDIS_LOCALLY = True 

# Option to run channels/cache on Redis locally (requires redis install)
if USE_REDIS_LOCALLY:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True, # Don't crash on say ConnectionError due to limits
            }
        }
    }

# ==============================================================================
# Django-specific Modules
# ==============================================================================

INTERNAL_IPS = (
    '0.0.0.0',
    '127.0.0.1'
)

# ==============================================================================
# Caching
# ==============================================================================

PUBLIC_FAST_CACHE_TIMEOUT   = 60
PUBLIC_SLOW_CACHE_TIMEOUT   = 60
TAB_PAGES_CACHE_TIMEOUT     = 60

CACHES = { # Use a dummy cache in development
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
   }
}
ALLOWED_HOSTS = ["*"]


# Use the cache with database write through for local sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
