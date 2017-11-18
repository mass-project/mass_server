from mongoengine import DateTimeField, ReferenceField, IntField

from mass_server.core.utils import TimeFunctions
from mass_server import db
from .analysis_system_instance import AnalysisSystemInstance
from .sample import Sample


class ScheduledAnalysis(db.Document):
    analysis_system_instance = ReferenceField(AnalysisSystemInstance, required=True)
    sample = ReferenceField(Sample, required=True)
    analysis_scheduled = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    priority = IntField(default=0, required=True)

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

    # @staticmethod
    # def get_count_for_instance(instance):
    #     analyses_count = ScheduledAnalysis.objects(analysis_system_instance=instance).count()
    #     return analyses_count

    # @staticmethod
    # def get_count_for_all_instances():
    #     instance_counts = dict()
    #     for item in AnalysisSystemInstance.objects:
    #         instance_counts[item] = 0
    #     for item in ScheduledAnalysis.objects:
    #         instance_counts[item.analysis_system_instance] += 1
    #     return instance_counts
