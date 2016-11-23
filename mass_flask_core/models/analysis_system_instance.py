from uuid import uuid4
from flask_modular_auth import AbstractAuthEntity
from mass_flask_config.app import db
from mongoengine import StringField, DateTimeField, ReferenceField
from mass_flask_core.utils import TimeFunctions
from .analysis_system import AnalysisSystem
from .tlp_level import TLPLevelField
import datetime


def _gen_uuid():
    return str(uuid4())


class AnalysisSystemInstance(db.Document, AbstractAuthEntity):
    @property
    def is_authenticated(self):
        return True

    def get_roles(self):
        return ['analysis_system_instance']

    @property
    def max_tlp_level(self):
        return TLPLevelField.TLP_LEVEL_WHITE

    analysis_system = ReferenceField(AnalysisSystem, required=True)
    uuid = StringField(max_length=36, required=True, unique=True, default=_gen_uuid)
    last_seen = DateTimeField()

    meta = {
        'ordering': ['analysis_system', 'uuid'],
        'indexes': [('analysis_system', 'uuid')]
    }

    def __repr__(self):
        return '[AnalysisSystemInstance] {} {}'.format(self.analysis_system.identifier_name, self.uuid)

    def __str__(self):
        return self.__repr__()

    def update_last_seen(self):
        self.last_seen = TimeFunctions.get_timestamp()
        self.save()

    @property
    def is_online(self):
        if self.last_seen is None:
            return False

        difference = TimeFunctions.get_timestamp() - self.last_seen
        return difference < datetime.timedelta(minutes=10)
