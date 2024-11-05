from .base import *


DEBUG = False

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "tmp/django.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["warning"],
            "level": "INFO",
            "propagate": True,
        },
    },
}