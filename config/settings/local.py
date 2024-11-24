from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS += [  # noqa: F405
    "http://localhost:8080",
    "http://192.168.1.66:8080",
    "http://localhost:8081",
    "http://192.168.1.66:8081",
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
