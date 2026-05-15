from .base import *

from logging import getLogger
logger = getLogger(__name__)
logger.warning("Loading local.py")

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

import os
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'static'),
]

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'