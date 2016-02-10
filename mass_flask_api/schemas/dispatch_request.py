from marshmallow.fields import Nested
from mass_flask_api.config import api_blueprint
from .sample import SampleSchema
from .base import BaseSchema, ForeignReferenceField
from mass_flask_core.models import DispatchRequest, Sample
from flask.ext.marshmallow.fields import URLFor


class DispatchRequestSchema(BaseSchema):
    url = URLFor('.dispatch_request', id='<id>', _external=True)
    # sample = ForeignReferenceField(endpoint='mass_flask_api.sample', queryset=Sample.objects(), query_parameter='id')
    sample = Nested(SampleSchema)

    class Meta(BaseSchema.Meta):
        model = DispatchRequest
        dump_only = [
            'id',
            '_cls',
            'dispatch_requested'
        ]

api_blueprint.apispec.definition('DispatchRequest', schema=DispatchRequestSchema)
