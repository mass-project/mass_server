from mass_flask_config.app import db
from mongoengine import StringField, DateTimeField, ReferenceField
from mass_flask_core.utils import TimeFunctions
from .analysis_system import AnalysisSystem
import datetime


class AnalysisSystemInstance(db.Document):
    analysis_system = ReferenceField(AnalysisSystem, required=True)
    uuid = StringField(max_length=36, required=True, unique=True)
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

        print(TimeFunctions.get_timestamp())
        print(self.last_seen)
        difference = TimeFunctions.get_timestamp() - self.last_seen
        return difference < datetime.timedelta(minutes=10)
