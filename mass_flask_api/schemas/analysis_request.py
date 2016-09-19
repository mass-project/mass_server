from mass_flask_api.config import api_blueprint
from .base import BaseSchema, ForeignReferenceField
from mass_flask_core.models import AnalysisRequest, AnalysisSystem, Sample
from flask_marshmallow.fields import URLFor


class AnalysisRequestSchema(BaseSchema):
    url = URLFor('.analysis_request_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', queryset=Sample.objects(), query_parameter='id')
    analysis_system = ForeignReferenceField(endpoint='.analysis_system_detail', queryset=AnalysisSystem.objects(), query_parameter='identifier_name')

    class Meta(BaseSchema.Meta):
        model = AnalysisRequest
        dump_only = [
            'id',
            '_cls',
            'analysis_requested'
        ]

api_blueprint.apispec.definition('AnalysisRequest', schema=AnalysisRequestSchema)
