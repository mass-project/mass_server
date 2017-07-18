from mongoengine import StringField
from mass_flask_config.app import db

class DBSchemaVersion(db.Document):
    version_string = StringField
