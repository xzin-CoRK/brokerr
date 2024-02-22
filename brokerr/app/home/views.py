from flask import Blueprint, render_template

import sys
sys.path.append('/brokerr')
from data import dataLayer
from utils import common

home_bp = Blueprint("home", __name__, template_folder="../templates")

@home_bp.route('/')
def home():

    # Set up the database and screenshot directory
    common.create_base_screenshot_directory()

    # Get the config
    trackers = dataLayer.get_trackers()
   
    return render_template('index.html', has_trackers = len(trackers) > 0, trackers = trackers)