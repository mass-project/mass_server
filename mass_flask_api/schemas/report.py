from mass_flask_api.config import api_blueprint
from .base import DynamicBaseSchema, ForeignReferenceField, BaseSchema
from mass_flask_core.models import AnalysisSystem, Sample, Report
from flask.ext.marshmallow.fields import URLFor


class ReportSchema(DynamicBaseSchema):
    url = URLFor('.report', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='mass_flask_api.sample', queryset=Sample.objects(), query_parameter='id')
    analysis_system = ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name')

    class Meta(BaseSchema.Meta):
        model = Report
        dump_only = [
            'id',
            '_cls',
            'report_date',
            'status'
        ]

api_blueprint.apispec.definition('Report', schema=ReportSchema)
