from flask import Flask, render_template, url_for, send_from_directory, request, jsonify
import os
from datetime import datetime

import sys
sys.path.append('/brokerr')
from common import setup
from common import yamlLayer
from common import common
from worker import brokerr

app = Flask(__name__, template_folder='/brokerr/app/templates')

@app.route('/images')
def get_image():
    '''Returns a screenshot based on the tracker name and filename query string arguments'''
    tracker_name = request.args.get('tracker_name')
    filename = request.args.get('filename')

    images_folder = f"/config/screenshots/{tracker_name}/"
    return send_from_directory(images_folder, filename)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/')
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
    

@app.route('/tracker/<tracker_name>')
def tracker(tracker_name):

    # load tracker stats from db
    last_insured = None
    num_insured = None
    res = setup.get_tracker_stats(tracker_name)
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


@app.route('/captureProof', methods=['POST'])
def captureProof():
    data = request.get_json()
    tracker = data.get('tracker')

    response = {}
    
    with brokerr.brokerrWorker() as worker:
        response = worker.captureScreenshots(tracker)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')