from flask_marshmallow.fields import URLFor

from mass_server.core.models import AnalysisSystem, Sample, Report
from mass_server.api.config import api_blueprint
from .base import ForeignReferenceField, BaseSchema, FileMapField


class ReportSchema(BaseSchema):
    url = URLFor('.report_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', model_class=Sample, query_parameter='id')
    analysis_system = ForeignReferenceField(endpoint='.analysis_system_detail', model_class=AnalysisSystem, query_parameter='identifier_name')
    json_report_objects = FileMapField(endpoint='.json_report_object', file_url_key='object_name')
    raw_report_objects = FileMapField(endpoint='.raw_report_object', file_url_key='object_name')

    class Meta(BaseSchema.Meta):
        model = Report
        dump_only = [
            'id',
            '_cls',
            'upload_date',
            'status'
        ]

api_blueprint.apispec.definition('Report', schema=ReportSchema)
