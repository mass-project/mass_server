from flask.ext.login import UserMixin, AnonymousUserMixin
from mongoengine import StringField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash

from mass_flask_config.app import db


class User(db.Document, UserMixin):
    username = StringField(min_length=3, max_length=50, unique=True, required=True)
    password_hash = StringField(min_length=5, max_length=200)
    _is_admin = BooleanField(default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self._is_admin


class AnonymousUser(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

