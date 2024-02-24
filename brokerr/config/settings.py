from distutils.util import strtobool
import os

DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

SECRET_KEY = os.environ["SECRET_KEY"]

# Redis
REDIS_URL = "redis://127.0.0.1:6379/0"

# SQL Alchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:////config/brokerr.db'

# Celery
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "worker_concurrency": 4,
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