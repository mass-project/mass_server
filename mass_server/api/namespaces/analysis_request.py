from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate

from mass_server.api.config import api
from mass_server.api.schemas import AnalysisRequestSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import AnalysisRequest


@api.add_namespace('/analysis_request')
class AnalysisRequestNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(AnalysisRequestSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return AnalysisRequest.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(AnalysisRequestSchema(), return_code=201)
    @load(AnalysisRequestSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(AnalysisRequest.DoesNotExist,
           'No analysis request with the specified id found.', 404)
    @dump(AnalysisRequestSchema())
    def element_get(self, id):
        return AnalysisRequest.objects.get(id=id)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(AnalysisRequest.DoesNotExist,
           'No analysis request with the specified id found.', 404)
    def element_delete(self, id):
        obj = AnalysisRequest.objects.get(id=id)
        obj.delete()
        return '', 204
