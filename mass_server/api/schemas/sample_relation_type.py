from flask_marshmallow.fields import URLFor
from mass_server.core.models import SampleRelationType
from .base import BaseSchema


class SampleRelationTypeSchema(BaseSchema):
    url = URLFor('api.sample_relation_type_namespace_element_get', name='<name>', _external=True)

    class Meta(BaseSchema.Meta):
        model = SampleRelationType
        dump_only = ['id']
