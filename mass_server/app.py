import os
import random

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_modular_auth import SessionBasedAuthProvider, KeyBasedAuthProvider

from mass_server.__version__ import __version__
from mass_server import db, auth
from mass_server.core.models import AnonymousUser, User, APIKey

from mass_server.core.signals import connect_signals
from mass_server.api.config import api_blueprint
from mass_server.webui.config import webui_blueprint

import mass_server.queue.queue_context as queue_context

from raven.contrib.flask import Sentry
from raven.transport.requests import RequestsHTTPTransport

from werkzeug.wsgi import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY as prometheus_registry
from mass_server.core.utils.metrics import DatabaseCollector

sentry = None


# Default configuration settings
class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    LOGGER_NAME = 'mass_server_flask'
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_USE_MINIFIED = True
    OBJECTS_PER_PAGE = 100
    MAX_SCHEDULE_THRESHOLD = 100
    SCHEDULE_ANALYSES_INTERVAL = 5


# Generate or load secret key
def _load_or_generate_secret_key(app):
    # Check if the secret is set in the environment variables
    env_secret = os.getenv('FLASK_SECRET', None)
    if env_secret:
        app.secret_key = env_secret
        return

    # If not try to read it from file
    secret_file_name = 'secret.txt'
    try:
        app.secret_key = app.open_instance_resource(
            secret_file_name).read().strip()
    except IOError:
        try:
            app.secret_key = ''.join([
                random.SystemRandom().choice(
                    'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                for i in range(50)
            ])
            secret = app.open_instance_resource(secret_file_name, 'w')
            secret.write(app.secret_key)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
            to generate your secret key!' % secret_file_name)


# Init Sentry
def _init_sentry(app):
    global sentry
    sentry_dsn = os.getenv('SENTRY_DSN', None)
    if sentry_dsn:
        sentry = Sentry()
        app.config['RAVEN_CONFIG'] = {
            'dsn': sentry_dsn,
            'transport': RequestsHTTPTransport
        }
        sentry.init_app(app)


# Load config
def _load_config(app, debug=False, testing=False):
    app.config.from_object(DefaultConfig)
    if testing == True:
        app.config['TESTING'] = True
    if debug == True:
        app.config['DEBUG'] = True

    mongo_host = os.getenv('MONGO_HOST', None)
    if mongo_host:
        app.config['MONGODB_SETTINGS'] = {
            'host': mongo_host,
            'tz_aware': True
        }

    app.config['AMQP_URL'] = os.getenv('AMQP_URL', 'amqp://guest:guest@localhost:5672/')
    app.config['AMQP_PREFETCH_COUNT'] = int(os.getenv('AMQP_PREFETCH_COUNT', '1'))
    app.config['WEBSTOMP_URL'] = os.getenv('WEBSTOMP_URL', 'ws://localhost:15674/ws/')

    try:
        if testing == False:
            app.config.from_pyfile('application.cfg')
        else:
            app.config.from_pyfile('testing.cfg')
    except FileNotFoundError:
        print('Could not load config file. Using default config.')


# Bootstrap app
def _bootstrap_app(app):
    # Init database
    db.init_app(app)

    # Load flask-bootstrap
    Bootstrap(app)

    # Init auth system
    auth.init_app(app)
    auth.set_unauthenticated_entity_class(AnonymousUser)
    app.session_provider = SessionBasedAuthProvider(User.user_loader)
    auth.register_auth_provider(app.session_provider)
    app.key_based_provider = KeyBasedAuthProvider(APIKey.api_key_loader)
    auth.register_auth_provider(app.key_based_provider)

    # Set the version number.
    app.version = __version__

    # Init blueprints and signals.
    connect_signals()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(webui_blueprint, url_prefix='/webui')

    # Init queue connection
    queue_context.start_connection(app.config['AMQP_URL'], app.config['AMQP_PREFETCH_COUNT'])

    # Add generic views
    @app.route('/version/', methods=['GET'])
    def get_version():
        return app.version

    @app.route('/', methods=['GET'])
    def index():
        return redirect(url_for('webui.index'))


def get_app(instance_path=None, testing=False, debug=False, set_server_name=False):
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
    _init_sentry(app)
    _load_or_generate_secret_key(app)
    _load_config(app, debug=debug, testing=testing)
    _bootstrap_app(app)

    if set_server_name:
        app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', '127.0.0.1:8000')
        print('Set server name to {}'.format(app.config['SERVER_NAME']))

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    prometheus_registry.register(DatabaseCollector())

    return app
