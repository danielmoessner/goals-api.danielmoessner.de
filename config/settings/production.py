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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = (
    f"goals.danielmoessner.de <{get_secret('EMAIL_ADDRESS')}>"  # noqa: F405
)
EMAIL_HOST = get_secret("EMAIL_HOST")  # noqa: F405
SERVER_EMAIL = get_secret("EMAIL_ADDRESS")  # noqa: F405
EMAIL_PORT = get_secret("EMAIL_PORT")  # noqa: F405
EMAIL_HOST_USER = get_secret("EMAIL_USER")  # noqa: F405
EMAIL_HOST_PASSWORD = get_secret("EMAIL_PASSWORD")  # noqa: F405
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
