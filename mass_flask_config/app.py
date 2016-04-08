import os
import subprocess
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mongoengine import MongoEngine
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

# Init db
db = MongoEngine(app)

# Init flask-bootstrap
Bootstrap(app)

# Load app version from git
app.version = subprocess.check_output(['git', 'describe'], cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).decode().strip()
