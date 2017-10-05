from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, load_json, catch, paginate
from flask_slimrest.utils import make_api_error_response

from mass_server.api.config import api
from mass_server.api.schemas import AnalysisSystemInstanceSchema, ScheduledAnalysisSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import AnalysisSystemInstance, ScheduledAnalysis


@api.add_namespace('/analysis_system_instance')
class AnalysisSystemInstanceNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(AnalysisSystemInstanceSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return AnalysisSystemInstance.objects

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/', methods=['POST'])
    @dump(AnalysisSystemInstanceSchema(), return_code=201)
    @load(AnalysisSystemInstanceSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<uuid>/')
    @catch(AnalysisSystemInstance.DoesNotExist,
           'No analysis system instance with the specified uuid found.', 404)
    @dump(AnalysisSystemInstanceSchema())
    def element_get(self, uuid):
        return AnalysisSystemInstance.objects.get(uuid=uuid)

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<uuid>/scheduled_analyses/')
    @catch(AnalysisSystemInstance.DoesNotExist,
           'No analysis system instance with the specified uuid found.', 404)
    @dump(ScheduledAnalysisSchema(), paginated=True)
    @paginate(pagination_helper)
    def element_analyses(self, uuid):
        instance = AnalysisSystemInstance.objects.get(uuid=uuid)
        instance.update_last_seen()
        analyses = ScheduledAnalysis.objects(analysis_system_instance=instance)
        return analyses

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<uuid>/', methods=['DELETE'])
    @catch(AnalysisSystemInstance.DoesNotExist,
           'No analysis system instance with the specified uuid found.', 404)
    def element_delete(self, uuid):
        obj = AnalysisSystemInstance.objects.get(uuid=uuid)
        obj.delete()
        return '', 204
