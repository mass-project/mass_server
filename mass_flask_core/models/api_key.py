from mongoengine import DateTimeField, ListField, StringField, ReferenceField
from itsdangerous import URLSafeSerializer as Serializer, BadSignature
from mass_flask_core.utils.time_functions import TimeFunctions
from mass_flask_config.app import db, app
from mass_flask_core.models import User, AnalysisSystemInstance

API_SCOPES = [
    'view_sample',
    'submit_sample',
]


class APIKey(db.Document):
    expiry_date = DateTimeField()
    scopes = ListField(StringField(choices=API_SCOPES))

    meta = {
        'allow_inheritance': True,
    }

    def is_expired(self):
        if self.expiry_date is not None and TimeFunctions.get_timestamp() >= self.expiry_date:
            return True
        else:
            return False

    def generate_auth_token(self):
        if self.id:
            s = Serializer(app.secret_key)
            return s.dumps(str(self.id))
        else:
            raise ValueError('APIKey must be saved before requesting an auth token.')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.secret_key)
        try:
            data = s.loads(token)
            api_key = APIKey.objects(id=data).first()
            if api_key.is_expired():
                api_key.delete()
                return None
            return api_key
        except BadSignature:
            return None  # invalid token


class UserAPIKey(APIKey):
    user = ReferenceField(User, required=True)

    @staticmethod
    def get_or_create(user):
        api_key = UserAPIKey.objects(user=user.id).first()
        if not api_key:
            api_key = UserAPIKey(user=user.id)
            api_key.save()
        return api_key


class InstanceAPIKey(APIKey):
    instance = ReferenceField(AnalysisSystemInstance, required=True)

    @staticmethod
    def get_or_create(instance):
        api_key = InstanceAPIKey.objects(instance=instance.id).first()
        if not api_key:
            api_key = InstanceAPIKey(instance=instance.id)
            api_key.save()
        return api_key


class APIKeyPrivilege:
    @staticmethod
    def check(api_key):
        raise NotImplementedError('Privilege check not implemented for generic class APIKeyPrivilege')


class AdminPrivilege(APIKeyPrivilege):
    @staticmethod
    def check(api_key):
        if not isinstance(api_key, UserAPIKey):
            return False
        return api_key.user.is_admin


class ValidUserPrivilege(APIKeyPrivilege):
    @staticmethod
    def check(api_key):
        return isinstance(api_key, UserAPIKey)


class ValidInstancePrivilege(APIKeyPrivilege):
    @staticmethod
    def check(api_key):
        return isinstance(api_key, InstanceAPIKey)
