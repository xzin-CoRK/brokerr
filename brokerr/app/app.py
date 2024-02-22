from celery import Celery
from celery import Task
from flask import Blueprint, Flask, render_template
import secrets

from data import dataLayer
from data.model import User, Tracker, Insurance

# Import views
from app.auth.views import auth_blueprint
from app.api.views import api_blueprint
from app.home.views import home_bp
from app.tracker.views import tracker_bp
from app.settings.views import settings_blueprint

# Import extensions
from app.extensions import db
from app.extensions import debug_toolbar
from app.extensions import login_manager

static_pages = Blueprint("static_pages", __name__)


def create_celery_app(app=None):
    """
    Create a new Celery app and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
        
        # Override the after_return method so that it logs the last successful run in the sqlite database
        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            with open("/config/celery.log", "a") as file:
                file.write(f"Task {self.name} just finished | task id: {task_id} | status: {status}\n")

    celery = Celery(app.import_name, task_cls=FlaskTask)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    celery.set_default()
    app.extensions["celery"] = celery
    celery.autodiscover_tasks(["worker"])

    return celery

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, template_folder="/brokerr/app/templates", static_folder="/brokerr/app/static")

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    # middleware(app)
        
    # Context processor to make APP_VERSION available to all templates
    @app.context_processor
    def inject_version():
        return dict(app_version=app.config.get('APP_VERSION', 'unknown'))

    # Register the blueprints
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(home_bp)
    app.register_blueprint(tracker_bp)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(static_pages)


    # the toolbar is only enabled in debug mode:
    app.debug = True

    # set a 'SECRET_KEY' to enable the Flask session cookies
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

    # Initialize the extensions
    extensions(app)

    # Initialize the database tables
    with app.app_context():
        db.create_all()

    return app

def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    
    debug_toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Redirect unauthenticated requests to the login page
    login_manager.login_view = 'auth.login'

    return None

# region Simple Routes
@static_pages.route('/help')
def help():
    return render_template('help.html')
#endregion

celery_app = create_celery_app()