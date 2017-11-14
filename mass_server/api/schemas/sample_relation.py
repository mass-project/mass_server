from flask_marshmallow.fields import URLFor
from mass_server.core.models import Sample, SampleRelation, SampleRelationType
from .base import BaseSchema, ForeignReferenceField


class SampleRelationSchema(BaseSchema):
    url = URLFor('api.sample_relation_namespace_element_get', id='<id>', _external=True)
    sample = ForeignReferenceField(
        endpoint='api.sample_namespace_element_get',
        model_class=Sample,
        query_parameter='id')
    other = ForeignReferenceField(
        endpoint='api.sample_namespace_element_get',
        model_class=Sample,
        query_parameter='id')
    relation_type = ForeignReferenceField(
        endpoint='api.sample_relation_type_namespace_element_get',
        model_class=SampleRelationType,
        query_parameter='name')

    class Meta(BaseSchema.Meta):
        model = SampleRelation
        dump_only = ['id']
