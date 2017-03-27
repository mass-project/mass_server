from flask_marshmallow.fields import URLFor

from mass_server.core.models import AnalysisSystem
from mass_server.api.config import api_blueprint
from mass_server.api.schemas import BaseSchema


class AnalysisSystemSchema(BaseSchema):
    url = URLFor('.analysis_system_detail', identifier_name='<identifier_name>', _external=True)

    class Meta(BaseSchema.Meta):
        model = AnalysisSystem
        dump_only = [
            'id',
            '_cls',
        ]

api_blueprint.apispec.definition('AnalysisSystem', schema=AnalysisSystemSchema)
