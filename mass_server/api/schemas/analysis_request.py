from flask_marshmallow.fields import URLFor

from mass_server.core.models import AnalysisRequest, AnalysisSystem, Sample
from .base import BaseSchema, ForeignReferenceField


class AnalysisRequestSchema(BaseSchema):
    url = URLFor(
        'api.analysis_request_namespace_element_get',
        id='<id>',
        _external=True)

    sample = ForeignReferenceField(
        endpoint='api.sample_namespace_element_get',
        model_class=Sample,
        query_parameter='id')

    analysis_system = ForeignReferenceField(
        endpoint='api.analysis_system_namespace_element_get',
        model_class=AnalysisSystem,
        query_parameter='identifier_name')

    class Meta(BaseSchema.Meta):
        model = AnalysisRequest
        dump_only = ['id', 'analysis_requested']
