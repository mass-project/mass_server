from flask_marshmallow.fields import URLFor

from mass_server.core.models import ScheduledAnalysis, AnalysisSystemInstance, Sample
from .base import BaseSchema, ForeignReferenceField


class ScheduledAnalysisSchema(BaseSchema):
    url = URLFor(
        'api.scheduled_analysis_namespace_element_get',
        id='<id>',
        _external=True)

    sample = ForeignReferenceField(
        endpoint='api.sample_namespace_element_get',
        model_class=Sample,
        query_parameter='id')

    analysis_system_instance = ForeignReferenceField(
        endpoint='api.analysis_system_instance_namespace_element_get',
        model_class=AnalysisSystemInstance,
        query_parameter='uuid')

    class Meta(BaseSchema.Meta):
        model = ScheduledAnalysis
        dump_only = ['id', 'analysis_scheduled']
