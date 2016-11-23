from mass_flask_api.config import api_blueprint


def get_pagination_compatible_schema(schema_class):
    from marshmallow import Schema
    from marshmallow.fields import Nested, Int

    class PaginationCompatibleSchema(Schema):
        results = Nested(schema_class, many=True)
        next = Int()
        previous = Int()
    return PaginationCompatibleSchema()


def register_api_endpoint(endpoint_name, resource):
    endpoint_path = '/{}/'.format(endpoint_name)
    endpoint_detail_path = endpoint_path + '<{}>/'.format(resource.query_key_field)
    endpoint_detail_path_spec = endpoint_path + '{{{}}}/'.format(resource.query_key_field)
    resource_view = resource.as_view(endpoint_name)
    resource_detail_view = resource.as_view(endpoint_name + '_detail')
    api_blueprint.add_url_rule(endpoint_path, view_func=resource_view, methods=['GET'])
    api_blueprint.add_url_rule(endpoint_path, view_func=resource_view, methods=['POST'])
    api_blueprint.add_url_rule(endpoint_detail_path, view_func=resource_detail_view, methods=['GET', 'PUT', 'DELETE'])
    api_blueprint.apispec.add_path(path=endpoint_path, view=resource.get_list)
    api_blueprint.apispec.add_path(path=endpoint_path, view=resource.post)
    api_blueprint.apispec.add_path(path=endpoint_detail_path_spec, view=resource.get_detail)
    api_blueprint.apispec.add_path(path=endpoint_detail_path_spec, view=resource.put)
    api_blueprint.apispec.add_path(path=endpoint_detail_path_spec, view=resource.delete)
