from flask_marshmallow.fields import URLFor

from mass_server.core.models import AnalysisSystem, Sample, Report
from .base import ForeignReferenceField, BaseSchema, FileMapField


class ReportSchema(BaseSchema):
    url = URLFor('api.report_namespace_element_get', id='<id>', _external=True)

    sample = ForeignReferenceField(
        endpoint='api.sample_namespace_element_get',
        model_class=Sample,
        query_parameter='id')

    analysis_system = ForeignReferenceField(
        endpoint='api.analysis_system_namespace_element_get',
        model_class=AnalysisSystem,
        query_parameter='identifier_name')

    json_report_objects = FileMapField(
        endpoint='.json_report_object', file_url_key='object_name')

    raw_report_objects = FileMapField(
        endpoint='.raw_report_object', file_url_key='object_name')

    class Meta(BaseSchema.Meta):
        model = Report
        dump_only = ['id', 'upload_date', 'status']
