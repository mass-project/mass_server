from mass_flask_api.config import api_blueprint
from .base import BaseSchema, ForeignReferenceField
from mass_flask_core.models import ScheduledAnalysis, AnalysisSystemInstance, Sample
from flask_marshmallow.fields import URLFor


class ScheduledAnalysisSchema(BaseSchema):
    url = URLFor('.scheduled_analysis_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', queryset=Sample.objects(), query_parameter='id')
    analysis_system_instance = ForeignReferenceField(endpoint='.analysis_system_instance_detail', queryset=AnalysisSystemInstance.objects(), query_parameter='uuid')

    class Meta(BaseSchema.Meta):
        model = ScheduledAnalysis
        dump_only = [
            'id',
            '_cls',
            'analysis_scheduled'
        ]

api_blueprint.apispec.definition('ScheduledAnalysis', schema=ScheduledAnalysisSchema)
