from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate

from mass_server.api.config import api
from mass_server.api.schemas import ReportSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import Report


@api.add_namespace('/report')
class ReportNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(ReportSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return Report.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(ReportSchema(), return_code=201)
    @load(ReportSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(Report.DoesNotExist, 'No report with the specified id found.', 404)
    @dump(ReportSchema())
    def element_get(self, id):
        return Report.objects.get(id=id)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(Report.DoesNotExist, 'No report with the specified id found.', 404)
    def element_delete(self, id):
        obj = Report.objects.get(id=id)
        obj.delete()
        return '', 204
