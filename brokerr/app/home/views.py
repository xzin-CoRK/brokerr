from flask import Blueprint, render_template

import sys
sys.path.append('/brokerr')
from common import setup
from common import yamlLayer

home_bp = Blueprint("home", __name__, template_folder="../templates")

@home_bp.route('/')
def home():

    # Set up the database and screenshot directory
    setup.setup_env()

    # Get the config
    config = yamlLayer.get_config()

    # If trackers exist, display the tracker overview
    if config and len(config['trackers']) > 0:
        return render_template('index.html', trackers = config['trackers'])
    else:
        return render_template('config-error.html')