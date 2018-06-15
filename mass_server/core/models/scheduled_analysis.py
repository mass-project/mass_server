from mongoengine import DateTimeField, ReferenceField, IntField, DictField

from mass_server.core.utils import TimeFunctions
from mass_server import db
from .analysis_system import AnalysisSystem
from .sample import Sample


class ScheduledAnalysis(db.Document):
    analysis_system = ReferenceField(AnalysisSystem, required=True)
    sample = ReferenceField(Sample, required=True)
    analysis_scheduled = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    priority = IntField(default=0, required=True)
    parameters = DictField()
    num_retry = IntField(min_value=0, default=0)

    filter_parameters = {
        'analysis_system_instance': None,
        'sample': None,
        'analysis_scheduled__lte': None,
        'analysis_scheduled__gte': None,
        'priority__lte': None,
        'priority__gte': None,
        'priority': None
    }

    meta = {
        'ordering': ['-analysis_scheduled'],
        'indexes': ['analysis_scheduled']
    }
