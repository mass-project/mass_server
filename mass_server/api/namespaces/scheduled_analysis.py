from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate

from mass_server.api.config import api
from mass_server.api.schemas import ScheduledAnalysisSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import ScheduledAnalysis


@api.add_namespace('/scheduled_analysis')
class ScheduledAnalysisNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(ScheduledAnalysisSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return ScheduledAnalysis.objects

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/', methods=['POST'])
    @dump(ScheduledAnalysisSchema(), return_code=201)
    @load(ScheduledAnalysisSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(ScheduledAnalysis.DoesNotExist,
           'No scheduled analysis with the specified id found.', 404)
    @dump(ScheduledAnalysisSchema())
    def element_get(self, id):
        return ScheduledAnalysis.objects.get(id=id)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(ScheduledAnalysis.DoesNotExist,
           'No scheduled analysis with the specified id found.', 404)
    def element_delete(self, id):
        obj = ScheduledAnalysis.objects.get(id=id)
        obj.delete()
        return '', 204
