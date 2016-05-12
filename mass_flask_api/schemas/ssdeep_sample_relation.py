from flask.ext.marshmallow.fields import URLFor
from marshmallow.fields import Float
from mass_flask_core.models import SsdeepSampleRelation
from mass_flask_core.models import Sample
from mass_flask_api.config import api_blueprint
from .base import BaseSchema
from .base import ForeignReferenceField


class SsdeepSampleRelationSchema(BaseSchema):
    url = URLFor('.ssdeep_sample_relation', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='mass_flask_api.sample', queryset=Sample.objects(), query_parameter='id')
    other = ForeignReferenceField(endpoint='mass_flask_api.sample', queryset=Sample.objects(), query_parameter='id')
    match = Float()

    class Meta(BaseSchema.Meta):
        model = SsdeepSampleRelation
        dump_only = [
                'id',
                '_cls',
                'sample',
                'other',
                'match',
                ]

api_blueprint.apispec.definition('SsdeepSampleRelation', schema=SsdeepSampleRelationSchema)
