from flask import Blueprint, render_template, request
from flask_login import login_required
from wtforms.form import Form
from data import dataLayer

settings_blueprint = Blueprint("settings", __name__, template_folder="../templates")

@settings_blueprint.route("/settings/trackers")
@login_required
def tracker_settings():
    is_master_password_set = dataLayer.is_master_key_set()
    return render_template('tracker_settings.html',
                           is_master_password_set=is_master_password_set,
                           button_disabled = not is_master_password_set)

@settings_blueprint.route("/settings/tasks")
@login_required
def tasks():
    return render_template('tasks.html')

@settings_blueprint.route("/settings/password")
@login_required
def master_password():
    is_master_password_set = dataLayer.is_master_key_set()
    return render_template('password.html', is_master_password_set = is_master_password_set)

@settings_blueprint.route("/settings/clients")
@login_required
def torrent_clients():
    is_master_password_set = dataLayer.is_master_key_set()
    return render_template('torrent_clients.html',
                           is_master_password_set=is_master_password_set,
                           button_disabled = not is_master_password_set)

@settings_blueprint.route('/updatePassword', methods=['POST'])
@login_required
def update_password():
    data = request.get_json()
    old_pass = data['old_password'] or None
    new_pass = data['new_password']
    # TODO