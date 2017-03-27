from itsdangerous import URLSafeSerializer as Serializer, BadSignature
from mongoengine import DateTimeField, ListField, StringField, ReferenceField

from mass_server.core.models import User, AnalysisSystemInstance
from mass_server.core.utils.time_functions import TimeFunctions
from mass_server.config.app import db, app, setup_key_based_auth

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

    @property
    def referenced_entity(self):
        return None

    @staticmethod
    def api_key_loader(key):
        s = Serializer(app.secret_key)
        try:
            data = s.loads(key)
            api_key = APIKey.objects(id=data).first()
            if api_key.is_expired():
                api_key.delete()
                return None
            else:
                return api_key.referenced_entity
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

    @property
    def referenced_entity(self):
        return self.user


class InstanceAPIKey(APIKey):
    instance = ReferenceField(AnalysisSystemInstance, required=True)

    @staticmethod
    def get_or_create(instance):
        api_key = InstanceAPIKey.objects(instance=instance.id).first()
        if not api_key:
            api_key = InstanceAPIKey(instance=instance.id)
            api_key.save()
        return api_key

    @property
    def referenced_entity(self):
        return self.instance

setup_key_based_auth(key_loader=APIKey.api_key_loader)
