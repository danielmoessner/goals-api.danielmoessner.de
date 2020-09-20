from .base import *

# Secret Settings

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

# Application definition

# INSTALLED_APPS = ['django_gulp'] + INSTALLED_APPS

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

# Other

INTERNAL_IPS = ["127.0.0.1", ]

# Gulp

# GULP_CWD = "'{}'".format(os.path.join(APPS_DIR, 'files'))
# GULP_DEVELOP_COMMAND = 'gulp --cwd {}'.format(GULP_CWD)
# GULP_PRODUCTION_COMMAND = 'gulp build --cwd {}'.format(GULP_CWD)  # to do

# Cors to allow my fronted app to make requests

CORS_ALLOWED_ORIGINS += [
    "http://localhost:8080",
    'http://192.168.1.66:8080'
]
