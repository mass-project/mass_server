from flask_marshmallow.fields import URLFor

from mass_server.core.models import ScheduledAnalysis, AnalysisSystemInstance, Sample
from mass_server.api.config import api_blueprint
from .base import BaseSchema, ForeignReferenceField


class ScheduledAnalysisSchema(BaseSchema):
    url = URLFor('.scheduled_analysis_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', model_class=Sample, query_parameter='id')
    analysis_system_instance = ForeignReferenceField(endpoint='.analysis_system_instance_detail', model_class=AnalysisSystemInstance, query_parameter='uuid')

    class Meta(BaseSchema.Meta):
        model = ScheduledAnalysis
        dump_only = [
            'id',
            '_cls',
            'analysis_scheduled'
        ]

api_blueprint.apispec.definition('ScheduledAnalysis', schema=ScheduledAnalysisSchema)
