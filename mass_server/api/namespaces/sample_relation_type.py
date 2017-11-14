from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate

from mass_server.api.config import api
from mass_server.api.schemas import SampleRelationTypeSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import SampleRelationType


@api.add_namespace('/sample_relation_type')
class SampleRelationTypeNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(SampleRelationTypeSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return SampleRelationType.objects

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/', methods=['POST'])
    @dump(SampleRelationTypeSchema(), return_code=201)
    @load(SampleRelationTypeSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<name>/')
    @catch(SampleRelationType.DoesNotExist, 'No relation type with the specified name found.', 404)
    @dump(SampleRelationTypeSchema())
    def element_get(self, name):
        return SampleRelationType.objects.get(name=name)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<name>/', methods=['DELETE'])
    @catch(SampleRelationType.DoesNotExist, 'No relation type with the specified name found.', 404)
    def element_delete(self, name):
        obj = SampleRelationType.objects.get(name=name)
        obj.delete()
        return '', 204
