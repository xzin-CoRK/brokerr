from datetime import datetime
from flask import Blueprint, render_template
import os

import sys
sys.path.append('/brokerr')

from data import dataLayer
from utils import common

tracker_bp = Blueprint("tracker", __name__, template_folder="../templates")

@tracker_bp.route('/tracker/<tracker_name>')
def tracker(tracker_name):

    # load tracker stats from db
    last_insured = None
    num_insured = None
    res = dataLayer.get_tracker_stats(tracker_name)
    if res:
        last_insured, num_insured = res

    # convert last_insured to a readable date
    if last_insured:
        last_insured = datetime.utcfromtimestamp(last_insured).strftime('%Y-%m-%d %H:%M:%S')

    # get images
    # TODO: use the database to get recent images
    images = []
    folder_path = f"/config/screenshots/{tracker_name}/"
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.png'):
                full_path = os.path.join(folder_path, filename)
                images.append({'filename': filename, 'path': full_path})
    except FileNotFoundError as ex:
        # TODO: Make sure we're creating the directory during initial config
        common.log_error("Tracker screenshot directory not created yet.")

    return render_template('tracker.html',
                           tracker = tracker_name,
                           has_images = len(images) > 0,
                           images = images,
                           last_insured = last_insured,
                           num_insured = num_insured)