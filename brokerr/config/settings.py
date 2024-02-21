import os
from distutils.util import strtobool

DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

# Redis
REDIS_URL = "redis://127.0.0.1:6379/0"

# Celery
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "include": [],
    "beat_logfile": "/config/debug.log",
    "beat_schedule": {
        'every-30-seconds': {
            'task': 'get_favicons',
            'schedule': 65.0
        }
    }
}

APP_VERSION = 'v0.2-alpha'