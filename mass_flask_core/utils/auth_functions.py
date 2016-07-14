import re
from flask import has_request_context, _request_ctx_stack, request, jsonify
from functools import wraps
from werkzeug.local import LocalProxy
from mass_flask_core.models import APIKey, UserAPIKey, InstanceAPIKey

current_api_key = LocalProxy(lambda: AuthFunctions.get_current_api_key())


class AuthFunctions:
    @staticmethod
    def get_current_api_key():
        if has_request_context() and not hasattr(_request_ctx_stack.top, 'api_key'):
            AuthFunctions._load_api_key()
        return _request_ctx_stack.top.api_key

    @staticmethod
    def _load_api_key():
        if 'Authorization' not in request.headers:
            _request_ctx_stack.top.api_key = None
            return
        authorization_header = request.headers['Authorization']
        m = re.match('^APIKEY (.*)$', authorization_header)
        if not m:
            _request_ctx_stack.top.api_key = None
            return
        token = m.group(1)
        api_key = APIKey.verify_auth_token(token)
        if not api_key:
            _request_ctx_stack.top.api_key = None
            return
        else:
            _request_ctx_stack.top.api_key = api_key
            return api_key

    @staticmethod
    def check_api_key_privileges(api_key, privileges=list(), check_mode='require_all'):
        if check_mode == 'require_all':
            for privilege in privileges:
                if not privilege.check(api_key):
                    return False
            return True
        elif check_mode == 'require_any':
            for privilege in privileges:
                if privilege.check(api_key):
                    return True
            return False
        else:
            raise ValueError('Invalid value for check_mode.')

    @staticmethod
    def check_api_key(privileges=list(), check_mode='require_all'):
        def real_decorator(fn):
            @wraps(fn)
            def inner(*args, **kwargs):
                if not AuthFunctions.get_current_api_key():
                    return jsonify({'error': 'Invalid API key. Provide a valid API key when accessing this resource.'}), 403
                if not AuthFunctions.check_api_key_privileges(AuthFunctions.get_current_api_key(), privileges, check_mode):
                    return jsonify({'error': 'API key has insufficient permissions to access this resource.'}), 403
                return fn(*args, **kwargs)

            return inner

        return real_decorator


class AccessPrivilege:
    def check(self, api_key):
        raise NotImplementedError('Privilege check not implemented for generic class APIKeyPrivilege')


class AdminAccessPrivilege(AccessPrivilege):
    def check(self, api_key):
        if not isinstance(api_key, UserAPIKey):
            return False
        return api_key.user.is_admin


class ValidUserAccessPrivilege(AccessPrivilege):
    def check(self, api_key):
        return isinstance(api_key, UserAPIKey)


class ValidInstanceAccessPrivilege(AccessPrivilege):
    def check(self, api_key):
        return isinstance(api_key, InstanceAPIKey)


class UUIDCheckAccessPrivilege(AccessPrivilege):
    def __init__(self, uuid_view_arg='uuid'):
        self._uuid_view_arg = uuid_view_arg

    def check(self, api_key):
        if isinstance(api_key, InstanceAPIKey) and api_key.instance.uuid == request.view_args[self._uuid_view_arg]:
            return True
        else:
            return False

