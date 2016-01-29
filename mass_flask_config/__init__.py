from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.debug = True

app.config['MONGODB_SETTINGS'] = {
    'db': 'flask-test',
    'host': 'localhost',
    'port': 27017,
    'tz_aware': True
}

db = MongoEngine(app)
