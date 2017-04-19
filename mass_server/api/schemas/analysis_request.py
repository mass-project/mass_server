from flask_marshmallow.fields import URLFor

from mass_server.core.models import AnalysisRequest, AnalysisSystem, Sample
from mass_server.api.config import api_blueprint
from .base import BaseSchema, ForeignReferenceField


class AnalysisRequestSchema(BaseSchema):
    url = URLFor('.analysis_request_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', model_class=Sample, query_parameter='id')
    # sample = URLFor('.sample_detail', id='<sample.id>', _external=True)
    analysis_system = ForeignReferenceField(endpoint='.analysis_system_detail', model_class=AnalysisSystem, query_parameter='identifier_name')

    class Meta(BaseSchema.Meta):
        model = AnalysisRequest
        dump_only = [
            'id',
            '_cls',
            'analysis_requested'
        ]

api_blueprint.apispec.definition('AnalysisRequest', schema=AnalysisRequestSchema)
