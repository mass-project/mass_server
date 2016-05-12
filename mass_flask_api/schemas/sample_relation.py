from flask.ext.marshmallow.fields import URLFor
from marshmallow.fields import String
from mass_flask_core.models import SampleRelation
from mass_flask_core.models import Sample
from mass_flask_api.config import api_blueprint
from .base import BaseSchema
from .base import ForeignReferenceField


class SampleRelationSchema(BaseSchema):
    url = URLFor('.sample_relation', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='mass_flask_api.sample', queryset=Sample.objects(), query_parameter='id')
    other = ForeignReferenceField(endpoint='mass_flask_api.sample', queryset=Sample.objects(), query_parameter='id')
    relation_type = String()

    class Meta(BaseSchema.Meta):
        model = SampleRelation
        dump_only = [
                'id',
                '_cls',
                'sample',
                'other',
                'relation_type',
                ]

api_blueprint.apispec.definition('SampleRelation', schema=SampleRelationSchema)
