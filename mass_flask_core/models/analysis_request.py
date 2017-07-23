from mass_flask_config.app import db
from .analysis_system import AnalysisSystem
from .sample import Sample
from mongoengine import DateTimeField, ReferenceField, IntField
from mass_flask_core.utils import TimeFunctions


class AnalysisRequest(db.Document):
    analysis_system = ReferenceField(AnalysisSystem, required=True)
    sample = ReferenceField(Sample, required=True)
    analysis_requested = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    priority = IntField(default=0, required=True)

    meta = {
        'ordering': ['-analysis_requested'],
        'indexes': ['analysis_requested']
    }

    def __repr__(self):
        return '[AnalysisRequest] {} on {}'.format(self.sample.id, self.analysis_system.identifier_name)

    def __str__(self):
        return self.__repr__()
