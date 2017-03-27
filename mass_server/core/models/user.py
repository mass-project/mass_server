from bson import ObjectId
from flask_modular_auth import AbstractAuthEntity
from mongoengine import StringField, IntField
from werkzeug.security import generate_password_hash, check_password_hash

from mass_server.config.app import db, setup_session_auth, auth_manager
from .tlp_level import TLPLevelField


class UserLevel:
    USER_LEVEL_ANONYMOUS = 0
    USER_LEVEL_USER = 1
    USER_LEVEL_PRIVILEGED = 2
    USER_LEVEL_MANAGER = 3
    USER_LEVEL_ADMIN = 4


class UserLevelField(IntField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [
            UserLevel.USER_LEVEL_ANONYMOUS,
            UserLevel.USER_LEVEL_USER,
            UserLevel.USER_LEVEL_PRIVILEGED,
            UserLevel.USER_LEVEL_MANAGER,
            UserLevel.USER_LEVEL_ADMIN
        ]
        super(UserLevelField, self).__init__(*args, **kwargs)


class UserMixin(AbstractAuthEntity):
    user_level = UserLevel.USER_LEVEL_ANONYMOUS

    def get_roles(self):
        roles = []
        if self.is_user:
            roles.append('user')
        if self.is_privileged:
            roles.append('privileged')
        if self.is_manager:
            roles.append('manager')
        if self.is_admin:
            roles.append('admin')
        return roles

    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return self.user_level == UserLevel.USER_LEVEL_ANONYMOUS

    @property
    def is_user(self):
        return self.user_level >= UserLevel.USER_LEVEL_USER

    @property
    def is_privileged(self):
        return self.user_level >= UserLevel.USER_LEVEL_PRIVILEGED

    @property
    def is_manager(self):
        return self.user_level >= UserLevel.USER_LEVEL_MANAGER

    @property
    def is_admin(self):
        return self.user_level >= UserLevel.USER_LEVEL_ADMIN

    @property
    def max_tlp_level(self):
        if self.is_admin:
            return TLPLevelField.TLP_LEVEL_RED
        elif self.is_privileged:
            return TLPLevelField.TLP_LEVEL_AMBER
        elif self.is_user:
            return TLPLevelField.TLP_LEVEL_GREEN
        else:
            return TLPLevelField.TLP_LEVEL_WHITE


class User(db.Document, UserMixin):
    def is_authenticated(self):
        return True

    username = StringField(min_length=3, max_length=50, unique=True, required=True)
    password_hash = StringField(min_length=5, max_length=200)
    user_level = UserLevelField(default=UserLevel.USER_LEVEL_USER, required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @staticmethod
    def user_loader(**kwargs):
        if 'username' in kwargs and 'password' in kwargs:
            user = User.objects(username=kwargs['username']).first()
            if user and user.check_password(kwargs['password']):
                return user
            else:
                return None
        elif 'id' in kwargs and kwargs['id']:
            return User.objects(id=ObjectId(kwargs['id'])).first()
        else:
            raise RuntimeError('This access method is not supported by the user loader.')


class AnonymousUser(UserMixin):
    @property
    def is_authenticated(self):
        return False


auth_manager.set_unauthenticated_entity_class(AnonymousUser)
setup_session_auth(user_loader=User.user_loader)
