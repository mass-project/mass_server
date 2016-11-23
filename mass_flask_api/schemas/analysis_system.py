from flask_marshmallow.fields import URLFor
from mass_flask_api.config import api_blueprint
from mass_flask_api.schemas.base import BaseSchema
from mass_flask_core.models import AnalysisSystem


class AnalysisSystemSchema(BaseSchema):
    url = URLFor('.analysis_system_detail', identifier_name='<identifier_name>', _external=True)

    class Meta(BaseSchema.Meta):
        model = AnalysisSystem
        dump_only = [
            'id',
            '_cls',
        ]

api_blueprint.apispec.definition('AnalysisSystem', schema=AnalysisSystemSchema)
