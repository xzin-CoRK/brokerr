from flask import Blueprint, render_template, request
from utils import dataLayer

settings_blueprint = Blueprint("settings", __name__, template_folder="../templates")

@settings_blueprint.route("/settings/trackers")
def tracker_settings():
    is_master_password_set = dataLayer.is_master_pass_set()
    return render_template('tracker_settings.html',
                           is_master_password_set=is_master_password_set,
                           button_disabled = not is_master_password_set)

@settings_blueprint.route("/settings/tasks")
def tasks():
    return render_template('tasks.html')

@settings_blueprint.route("/settings/password")
def master_password():
    is_master_password_set = dataLayer.is_master_pass_set()
    return render_template('password.html', is_master_password_set = is_master_password_set)

@settings_blueprint.route("/settings/clients")
def torrent_clients():
    is_master_password_set = dataLayer.is_master_pass_set()
    return render_template('torrent_clients.html',
                           is_master_password_set=is_master_password_set,
                           button_disabled = not is_master_password_set)

@settings_blueprint.route('/updatePassword', methods=['POST'])
def update_password():
    data = request.get_json()
    old_pass = data['old_password'] or None
    new_pass = data['new_password']
    return dataLayer.try_set_master_pass(old_pass, new_pass)