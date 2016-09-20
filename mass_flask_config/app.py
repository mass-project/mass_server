import os
import subprocess

from pymongo import MongoClient
from flask import Flask, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_modular_auth import AuthManager, current_authenticated_entity, SessionBasedAuthProvider, KeyBasedAuthProvider
from .reverse_proxy import ReverseProxied

# Initialize app
app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

# Generate or load secret key
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_FILE = os.path.join(BASE_DIR, 'secret.txt')
try:
    app.secret_key = open(SECRET_FILE).read().strip()
except IOError:
    try:
        import random
        app.secret_key = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
        secret = open(SECRET_FILE, 'w')
        secret.write(app.secret_key)
        secret.close()
    except IOError:
        Exception('Please create a %s file with random characters \
        to generate your secret key!' % SECRET_FILE)

# Load config
config_path = os.getenv('CONFIG_PATH', 'mass_flask_config.config_development.DevelopmentConfig')
app.config.from_object(config_path)


# Dirty monkey patching of MongoClient to enable tz_aware
_original_init = MongoClient.__init__


def _patched_init(*args, **kwargs):
    kwargs['tz_aware'] = True
    _original_init(*args, **kwargs)

MongoClient.__init__ = _patched_init

# Init db
db = MongoEngine(app)

# Init flask-bootstrap
Bootstrap(app)


# Init auth system
def setup_session_auth(user_loader):
    app.session_provider = SessionBasedAuthProvider(user_loader)
    auth_manager.register_auth_provider(app.session_provider)


def setup_key_based_auth(key_loader):
    app.key_based_provider = KeyBasedAuthProvider(key_loader)
    auth_manager.register_auth_provider(app.key_based_provider)


def unauthorized_callback():
    if current_authenticated_entity.is_authenticated:
        flash('You are not authorized to access this resource!', 'warning')
        return redirect(url_for('mass_flask_webui.index'))
    else:
        return redirect(url_for('mass_flask_webui.login', next=request.url))

auth_manager = AuthManager(app, unauthorized_callback=unauthorized_callback)

# Load app version from git
app.version = subprocess.check_output(['git', 'describe'], cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).decode().strip()
