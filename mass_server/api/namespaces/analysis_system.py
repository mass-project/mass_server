from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, load_json, catch, paginate, filter_results
from flask_slimrest.utils import make_api_error_response

from mass_server.api.config import api
from mass_server.api.schemas import AnalysisSystemSchema
from mass_server.api.utils import pagination_helper, filter_queryset
from mass_server.core.models import AnalysisSystem


@api.add_namespace('/analysis_system')
class AnalysisSystemNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(AnalysisSystemSchema(), paginated=True)
    @paginate(pagination_helper)
    @filter_results(filter_queryset, [
        'identifier_name',
        'verbose_name',
        'identifier_name__contains',
        'verbose_name__contains'
    ])
    def collection_get(self):
        return AnalysisSystem.objects

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/', methods=['POST'])
    @dump(AnalysisSystemSchema(), return_code=201)
    @load(AnalysisSystemSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<identifier_name>/')
    @catch(AnalysisSystem.DoesNotExist,
           'No analysis system with the specified identifier_name found.', 404)
    @dump(AnalysisSystemSchema())
    def element_get(self, identifier_name):
        return AnalysisSystem.objects.get(identifier_name=identifier_name)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<identifier_name>/', methods=['PATCH'])
    @catch(AnalysisSystem.DoesNotExist,
           'No analysis system with the specified identifier_name found.', 404)
    @dump(AnalysisSystemSchema())
    @load_json
    def element_patch(self, identifier_name, data):
        obj = AnalysisSystem.objects.get(identifier_name=identifier_name)
        result = AnalysisSystemSchema().update(obj, data)
        if result.errors:
            return make_api_error_response(
                'Validation of the patched data has failed.', 400, {
                    'errors': result.errors
                })
        else:
            obj.save()
            return obj

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<identifier_name>/', methods=['DELETE'])
    @catch(AnalysisSystem.DoesNotExist,
           'No analysis system with the specified identifier_name found.', 404)
    def element_delete(self, identifier_name):
        obj = AnalysisSystem.objects.get(identifier_name=identifier_name)
        obj.delete()
        return '', 204
