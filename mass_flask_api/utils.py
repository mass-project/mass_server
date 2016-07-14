import re

from flask import request, jsonify
from functools import wraps

from mass_flask_api.config import api_blueprint
from mass_flask_core.models import APIKey


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
    api_blueprint.apispec.add_path(path=endpoint_path, view=resource.get_list)
    api_blueprint.apispec.add_path(path=endpoint_path, view=resource.post)
    api_blueprint.apispec.add_path(path=endpoint_detail_path_spec, view=resource.get_detail)
    api_blueprint.apispec.add_path(path=endpoint_detail_path_spec, view=resource.put)
    api_blueprint.apispec.add_path(path=endpoint_detail_path_spec, view=resource.delete)


def _get_and_check_api_key():
    if 'Authorization' not in request.headers:
        return None
    authorization_header = request.headers['Authorization']
    m = re.match('^APIKEY (.*)$', authorization_header)
    if not m:
        return None
    token = m.group(1)
    api_key = APIKey.verify_auth_token(token)
    if not api_key:
        return None
    else:
        return api_key


def _check_required_privileges(api_key, required_privileges):
    for privilege in required_privileges:
        if not privilege.check(api_key):
            return False
    return True


def check_api_key(required_privileges=[]):
    def real_decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            api_key = _get_and_check_api_key()
            if not api_key:
                return jsonify({'error': 'Invalid API key. Provide a valid API key when accessing this resource.'}), 403
            if not _check_required_privileges(api_key, required_privileges):
                return jsonify({'error': 'API key has insufficient permissions to access this resource.'}), 403
            return fn(*args, **kwargs)
        return inner
    return real_decorator
