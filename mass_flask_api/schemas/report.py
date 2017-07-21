from mass_flask_api.config import api_blueprint
from .base import ForeignReferenceField, BaseSchema, FileMapField
from mass_flask_core.models import AnalysisSystem, Sample, Report
from flask_marshmallow.fields import URLFor
from marshmallow.decorators import pre_dump


class ReportSchema(BaseSchema):
    url = URLFor('.report_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', queryset=Sample.objects(), query_parameter='id')
    analysis_system = ForeignReferenceField(endpoint='.analysis_system_detail', queryset=AnalysisSystem.objects(), query_parameter='identifier_name')
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

    @pre_dump
    def _clean_analysis_date(self, data):
        if data.analysis_date:
            data.analysis_date = data.analysis_date.replace(microsecond=0)
        return data

api_blueprint.apispec.definition('Report', schema=ReportSchema)
