from .base import *


# Secret Settings

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]


# Application definition

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]


# Other

INTERNAL_IPS = ["127.0.0.1", ]
