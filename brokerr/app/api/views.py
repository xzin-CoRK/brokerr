from datetime import datetime
from flask import Blueprint, jsonify, request, send_from_directory
import sys

sys.path.append('/brokerr')
from worker import brokerr

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route('/captureProof', methods=['POST'])
def captureProof():
    data = request.get_json()
    tracker = data.get('tracker')

    response = {}
    
    with brokerr.brokerrWorker() as worker:
        response = worker.captureScreenshots(tracker)

    return jsonify(response)

@api_blueprint.route('/images')
def get_image():
    '''Returns a screenshot based on the tracker name and filename query string arguments'''
    tracker_name = request.args.get('tracker_name')
    filename = request.args.get('filename')

    images_folder = f"/config/screenshots/{tracker_name}/"
    return send_from_directory(images_folder, filename)