from datetime import datetime
from flask import Blueprint, jsonify, request, send_from_directory, flash
from flask_login import login_required

from worker import brokerr
from data.model import Tracker
from utils import security
from app.extensions import db

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route('/captureProof', methods=['POST'])
@login_required
def captureProof():
    data = request.get_json()
    tracker = data.get('tracker')

    response = {}
    
    with brokerr.brokerrWorker() as worker:
        response = worker.captureScreenshots(tracker)

    return jsonify(response)

@api_blueprint.route('/images')
@login_required
def get_image():
    '''Returns a screenshot based on the tracker name and filename query string arguments'''
    tracker_name = request.args.get('tracker_name')
    filename = request.args.get('filename')

    images_folder = f"/config/screenshots/{tracker_name}/"
    return send_from_directory(images_folder, filename)

@api_blueprint.route('/addTracker', methods=['POST'])
@login_required
def add_tracker():
    data = request.get_json()
    tracker = Tracker()
    tracker.name = data.get('trackerName')
    tracker.login_url = data.get('loginUrl')
    tracker.screenshot_url = data.get('screenshot_url')

    credentials = {
        "username": data.get('username'),
        "password": data.get('password')
    }

    creds, salt = security.encrypt(str(credentials))
    tracker.credentials = creds
    tracker.salt = salt

    db.session.add(tracker)
    db.session.commit()

    flash((f"Tracker {tracker.name} successfully added!", 'success'))

    return jsonify({
            "success": True,
            "message": f"Tracker {tracker.name} successfully added!",
        })