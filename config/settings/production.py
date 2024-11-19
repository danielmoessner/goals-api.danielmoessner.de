from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")  # noqa: F405

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "tmp/django.log"),  # noqa: F405
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
