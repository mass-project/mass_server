from flask_marshmallow.fields import URLFor
from marshmallow.fields import Boolean, Method

from mass_server.core.models import AnalysisSystemInstance, AnalysisSystem, ScheduledAnalysis
from mass_server.api.config import api_blueprint
from mass_server.api.schemas import BaseSchema, ForeignReferenceField


class AnalysisSystemInstanceSchema(BaseSchema):
    url = URLFor('.analysis_system_instance_detail', uuid='<uuid>', _external=True)
    analysis_system = ForeignReferenceField(endpoint='.analysis_system_detail', model_class=AnalysisSystem, query_parameter='identifier_name')
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
