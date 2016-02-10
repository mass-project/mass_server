import os
import subprocess
from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
config_path = os.getenv('CONFIG_PATH', 'mass_flask_config.config_development.DevelopmentConfig')
app.config.from_object(config_path)
db = MongoEngine(app)
app.version = subprocess.check_output(['git', 'describe'], cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
