from apispec import APISpec
from flask import Blueprint, jsonify, url_for, _request_ctx_stack

api_blueprint = Blueprint('api', __name__)


class BasePathAPISpec(APISpec):
    def to_dict(self):
        result = super(BasePathAPISpec, self).to_dict()
        result['basePath'] = url_for('api.api_root')[:-1]
        return result


api_blueprint.apispec = BasePathAPISpec(
    title='MASS API',
    version='1.0',
    description='RESTful API to the MASS server.',
    plugins=[
        'apispec.ext.marshmallow',
    ],
)


@api_blueprint.route('/')
def api_root():
    return ''


@api_blueprint.route('/swagger/')
def swagger():
    return jsonify(api_blueprint.apispec.to_dict())


def api_unauthorized_callback():
    return jsonify({'error': 'You do not have access to this resource.'}), 403


@api_blueprint.before_request
def before_request_set_unauthorized_callback():
    ctx = _request_ctx_stack.top
    ctx.unauthorized_callback = api_unauthorized_callback
    return None
