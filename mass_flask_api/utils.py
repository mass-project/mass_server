from functools import wraps
from flask import request, url_for
from mass_flask_api.config import api_blueprint


def _get_page_link(page_number):
    return url_for(request.url_rule.endpoint, page=page_number, _external=True)


def paginate(view_function):
    @wraps(view_function)
    def paginate_function(*args, **kwargs):
        if 'page' in request.args:
            page = int(request.args['page'])
        else:
            page = 1
        queryset = view_function(*args, **kwargs)
        paginated_queryset = queryset.paginate(page=page, per_page=api_blueprint.config['OBJECTS_PER_PAGE'])
        result = {
            'results': paginated_queryset.items,
            'next': _get_page_link(paginated_queryset.next_num) if paginated_queryset.has_next else None,
            'previous': _get_page_link(paginated_queryset.prev_num) if paginated_queryset.has_prev else None,
        }
        return result
    return paginate_function


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
    api_blueprint.add_url_rule(endpoint_path, defaults={resource.query_key_field: None}, view_func=resource_view, methods=['GET'])
    api_blueprint.add_url_rule(endpoint_path, view_func=resource_view, methods=['POST'])
    api_blueprint.add_url_rule(endpoint_detail_path, view_func=resource_view, methods=['GET', 'PUT', 'DELETE'])
    api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + endpoint_path, view=resource.get_list)
    api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + endpoint_path, view=resource.post)
    api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + endpoint_detail_path_spec, view=resource.get_detail)
    api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + endpoint_detail_path_spec, view=resource.put)
    api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + endpoint_detail_path_spec, view=resource.delete)
