from mongoengine import StringField, DateTimeField, ReferenceField
from mass_flask_config.app import db
from .user import User
from mass_flask_core.utils import TimeFunctions


class Comment(db.EmbeddedDocument):
    comment = StringField(max_length=1000, verbose_name='Comment', help_text='Leave a comment', required=True)
    post_date = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    user = ReferenceField(User, required=True)
