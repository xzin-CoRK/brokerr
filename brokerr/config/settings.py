import os
from distutils.util import strtobool

DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

# SERVER_NAME = os.getenv(
#     "SERVER_NAME", "localhost:{0}".format(os.getenv("PORT", "6363"))
# )

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Celery
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "include": [],
}

APP_VERSION = 'v0.2-alpha'