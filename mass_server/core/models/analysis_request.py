from mongoengine import DateTimeField, ReferenceField, IntField, DictField
from datetime import datetime, timedelta

from mass_server.core.utils import TimeFunctions
from mass_server import db
from .analysis_system import AnalysisSystem
from .sample import Sample


class AnalysisRequest(db.Document):
    analysis_system = ReferenceField(AnalysisSystem, required=True)
    sample = ReferenceField(Sample, required=True)
    analysis_requested = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    schedule_after = DateTimeField(default=TimeFunctions.get_timestamp)
    priority = IntField(default=0, required=True)
    parameters = DictField()
    num_retry = IntField(min_value=0, default=0)

    filter_parameters = {
        'analysis_system': None,
        'sample': None,
        'analysis_requested__lte': None,
        'analysis_requested__gte': None,
        'schedule_after__lte': None,
        'schedule_after__gte': None,
        'priority__lte': None,
        'priority__gte': None,
        'priority': None
    }

    meta = {
        'ordering': ['-analysis_requested'],
        'indexes': ['analysis_requested', 'schedule_after']
    }

    def __repr__(self):
        return '[AnalysisRequest] {} on {}'.format(self.sample.id, self.analysis_system.identifier_name)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def create_from_scheduled_analysis(cls, scheduled_analysis, caused_by_failure=False):
        analysis_system = scheduled_analysis.analysis_system_instance.analysis_system

        if scheduled_analysis.num_retry + 1 >= analysis_system.number_retries and caused_by_failure:
            return None

        r = cls(analysis_system=analysis_system, sample=scheduled_analysis.sample,
                parameters=scheduled_analysis.parameters, priority=scheduled_analysis.priority,
                num_retry=scheduled_analysis.num_retry)

        if caused_by_failure:
            r.num_retry += 1
            r.schedule_after = datetime.now() + timedelta(minutes=analysis_system.minutes_before_retry)

        r.save()
        return r
