from flask_modular_auth import AbstractAuthEntity
from mongoengine import StringField, IntField, EmailField
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

from mass_flask_config.app import db, setup_session_auth, auth_manager
from .tlp_level import TLPLevelField

class UserLevel:
    """
    UserLevel provides constants for the different (integer) user levels

    User levels are internally handled as integer values. However, to avoid confusion about the meaning of each number, this class provides constant values with a meaningful name for each valid user level.
    """
    USER_LEVEL_ANONYMOUS = 0
    USER_LEVEL_USER = 1
    USER_LEVEL_PRIVILEGED = 2
    USER_LEVEL_MANAGER = 3
    USER_LEVEL_ADMIN = 4


class UserLevelField(IntField):
    """
    Mongoengine field for storing a UserLevel

    Technically, this is a :class:`mongoengine.fields.IntField`, but it only accepts integer values that correspond to a valid :class:`.UserLevel`.
    """
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
    """UserMixin

    The UserMixin class contains all properties and methods that are common for all types of users. It is an implementation of flask_modular_auth's :class:`flask_modular_auth.AbstractAuthEntity`.
    """
    user_level = UserLevel.USER_LEVEL_ANONYMOUS

    def get_roles(self):
        """Returns a list of string values representing the user's roles, i.e. 'manager', 'admin', etc."""
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
        """Returns true if the user is anonymous (i.e. a guest user)"""
        return self.user_level == UserLevel.USER_LEVEL_ANONYMOUS

    @property
    def is_user(self):
        """Returns true if the user is a normal (non-anonymous) user"""
        return self.user_level >= UserLevel.USER_LEVEL_USER

    @property
    def is_privileged(self):
        """Returns true if the user is a privileged user"""
        return self.user_level >= UserLevel.USER_LEVEL_PRIVILEGED

    @property
    def is_manager(self):
        """Retuns true if the user is a manager"""
        return self.user_level >= UserLevel.USER_LEVEL_MANAGER

    @property
    def is_admin(self):
        """Returns true if the user is an administrator"""
        return self.user_level >= UserLevel.USER_LEVEL_ADMIN

    @property
    def max_tlp_level(self):
        """Returns the maximum TLP access level granted for this user. By default, anonymous users will only be allowed to access content flagged with TLP label **WHITE**. Registered users may access content up to TLP level **GREEN**. Users with the user level 'privileged' may also access content with TLP level **YELLOW*. Administrators have access to all content in the system and thus can also see content labeled with TLP level **RED**. *Note that access to content with YELLOW and RED labels may also provided on a per-item access grant for specific users.*"""
        if self.is_admin:
            return TLPLevelField.TLP_LEVEL_RED
        elif self.is_privileged:
            return TLPLevelField.TLP_LEVEL_AMBER
        elif self.is_user:
            return TLPLevelField.TLP_LEVEL_GREEN
        else:
            return TLPLevelField.TLP_LEVEL_WHITE


class User(db.Document, UserMixin):
    """User

    A registered and authenticated user. This user type is used for all registered MASS users.
    """
    def is_authenticated(self):
        return True

    username = StringField(min_length=3, max_length=50, unique=True, required=True)
    password_hash = StringField(min_length=5, max_length=200)
    user_level = UserLevelField(default=UserLevel.USER_LEVEL_USER, required=True)
    email = EmailField()
    first_name = StringField(max_length=100)
    last_name = StringField(max_length=100)
    organization = StringField(max_length=100)

    def set_password(self, password):
        """Set the user password. The password will be hashed and salted using Werkzeug's :func:`werkzeug.security.generate_password_hash` method.

        :param password: The new password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the password of the user.

        :param password: The password to check
        """
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Get the string representation of the user's ObjectId"""
        return str(self.id)

    @staticmethod
    def user_loader(**kwargs):
        """Load a user from the database either by providing the ObjectId of that user or by providing the username and password. This method is used by flask_modular_auth to validate the login and to obtain the user data once the login is saved to the session.

        :param id: The ObjectId of the user (in string representation)
        :param username: The username to query from the database
        :param password: The password of the queried user
        :return: Returns the matching user or None if no matching user exists
        """
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
