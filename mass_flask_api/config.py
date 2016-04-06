from apispec import APISpec
from flask import Blueprint, jsonify, url_for

api_blueprint = Blueprint('mass_flask_api', __name__)

api_blueprint.config = {
    'OBJECTS_PER_PAGE': 100
}


class BasePathAPISpec(APISpec):
    def to_dict(self):
        result = super(BasePathAPISpec, self).to_dict()
        result['basePath'] = url_for('mass_flask_api.api_root')[:-1]
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
