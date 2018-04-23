from flask_marshmallow.fields import URLFor
from marshmallow.fields import List

from mass_server.core.models import Sample, AnalysisSystem
from .base import BaseSchema, ForeignReferenceField


class SampleSchema(BaseSchema):
    url = URLFor('api.sample_namespace_element_get', id='<id>', _external=True)
    delivery_dates = URLFor('api.sample_namespace_delivery_dates', id='<id>', _external=True)
    dispatched_to = List(
        ForeignReferenceField(
            endpoint='api.analysis_system_namespace_element_get',
            model_class=AnalysisSystem,
            query_parameter='identifier_name'))

    class Meta(BaseSchema.Meta):
        model = Sample
        exclude = ['created_by', 'comments']
        dump_only = ['id', 'dispatched_to', 'delivery_dates']
