from flask.ext.marshmallow.fields import URLFor
from marshmallow.fields import Boolean, Method

from mass_flask_api.config import api_blueprint
from mass_flask_api.schemas.base import BaseSchema, ForeignReferenceField
from mass_flask_core.models import AnalysisSystemInstance, AnalysisSystem, ScheduledAnalysis


class AnalysisSystemInstanceSchema(BaseSchema):
    url = URLFor('.analysis_system_instance', uuid='<uuid>', _external=True)
    analysis_system = ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name')
    is_online = Boolean()
    scheduled_analyses_count = Method("get_scheduled_analyses_count")

    class Meta(BaseSchema.Meta):
        model = AnalysisSystemInstance
        dump_only = [
            'id',
            '_cls',
            'last_seen',
            'scheduled_analyses_count'
        ]

    def get_scheduled_analyses_count(self, obj):
        analyses_count = ScheduledAnalysis.objects(analysis_system_instance=obj).count()
        return analyses_count

api_blueprint.apispec.definition('AnalysisSystemInstance', schema=AnalysisSystemInstanceSchema)
