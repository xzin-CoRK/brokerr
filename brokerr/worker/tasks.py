from celery import Celery
from celery.utils.log import get_task_logger
import os
import requests
import sys
from urllib.parse import urlsplit

logger = get_task_logger(__name__)

sys.path.append('/brokerr')
from utils import yamlLayer
from utils import dataLayer
from utils import common
from app.app import celery_app

@celery_app.task(name='get_favicons')
def get_favicons():
    print('get_favicons fired')
    
    # to_update = dataLayer.get_trackers_without_favicon()

    # # find the trackers that need updating
    # if to_update and len(to_update) > 0:

    #     # get the configs for the trackers that need updating
    #     config = yamlLayer.get_config()
    #     config_trackers = [t for t in config['trackers'] if t.get('name') in to_update]

    #     for tracker in config_trackers:
    #         split_url = urlsplit(tracker['login_url'])
    #         favicon_url = f"{split_url.scheme}://{split_url.netloc}/favicon.ico"
    #         res = requests.get(favicon_url)
    #         if res.status_code == 200:
    #             with open(f"/config/cache/{tracker.get('name')}.ico", "wb") as file:
    #                 file.write(res.content)
