from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate

from mass_server.api.config import api
from mass_server.api.schemas import SampleRelationSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import SampleRelation


@api.add_namespace('/sample_relation')
class SampleRelationNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(SampleRelationSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return SampleRelation.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(SampleRelationSchema(), return_code=201)
    @load(SampleRelationSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(SampleRelation.DoesNotExist, 'No sample relation with the specified id found.', 404)
    @dump(SampleRelationSchema())
    def element_get(self, id):
        return SampleRelation.objects.get(id=id)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(SampleRelation.DoesNotExist, 'No sample relation with the specified id found.', 404)
    def element_delete(self, id):
        obj = SampleRelation.objects.get(id=id)
        obj.delete()
        return '', 204
