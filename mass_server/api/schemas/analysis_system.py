from flask_marshmallow.fields import URLFor

from mass_server.core.models import AnalysisSystem
from mass_server.api.schemas import BaseSchema


class AnalysisSystemSchema(BaseSchema):
    url = URLFor(
        'api.analysis_system_namespace_element_get',
        identifier_name='<identifier_name>',
        _external=True)

    class Meta(BaseSchema.Meta):
        model = AnalysisSystem
        dump_only = ['id', 'url']
