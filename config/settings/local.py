from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS += [
    "http://localhost:8080",
    "http://192.168.1.66:8080",
    "http://localhost:8081",
    "http://192.168.1.66:8081",
]
