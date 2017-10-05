import os
import subprocess
import random

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_modular_auth import SessionBasedAuthProvider, KeyBasedAuthProvider

from mass_server import db, auth
from mass_server.core.models import AnonymousUser, User, APIKey

from mass_server.core.signals import connect_signals
from mass_server.api.config import api_blueprint
from mass_server.scheduling.config import scheduling_blueprint
from mass_server.webui.config import webui_blueprint


# Generate or load secret key
def _load_or_generate_secret_key(app):
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


# Load config
def _load_config(app, config_object, load_instance_config=False):
    app.config.from_object(config_object)
    if load_instance_config:
        app.config.from_pyfile('application.cfg')


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

    # Set the version number. For the future we should probably read it from a file.
    app.version = '1.0-alpha1'

    # Init blueprints and signals.
    connect_signals()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(webui_blueprint, url_prefix='/webui')
    app.register_blueprint(scheduling_blueprint, url_prefix='/scheduling')

    # Add generic views
    @app.route('/version/', methods=['GET'])
    def get_version():
        return app.version

    @app.route('/', methods=['GET'])
    def index():
        return redirect(url_for('webui.index'))


def _init_app(config_object, instance_path=None):
    app = Flask(__name__, instance_path=instance_path)
    _load_or_generate_secret_key(app)
    _load_config(app, config_object)
    _bootstrap_app(app)
    return app


def get_development_app():
    from mass_server.config.config_development import DevelopmentConfig
    return _init_app(DevelopmentConfig)


def get_testing_app():
    from mass_server.config.config_testing import TestingConfig
    return _init_app(TestingConfig)


def get_production_app(instance_path=None):
    from mass_server.config.config_production import ProductionConfig
    from mass_server.config.reverse_proxy import ReverseProxied
    return ReverseProxied(_init_app(ProductionConfig, instance_path))
