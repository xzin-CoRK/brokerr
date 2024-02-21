from flask import Blueprint, render_template

import sys
sys.path.append('/brokerr')
from utils import dataLayer
from utils import yamlLayer

home_bp = Blueprint("home", __name__, template_folder="../templates")

@home_bp.route('/')
def home():

    # Set up the database and screenshot directory
    dataLayer.setup_database()

    # Get the config
    config = yamlLayer.get_config()

    # If trackers exist:
    # Set up celery schedule and
    # display the tracker overview page
    if config and len(config['trackers']) > 0:

        return render_template('index.html', trackers = config['trackers'])
    else:
        return render_template('config-error.html')