from apispec import APISpec
from flask import Blueprint, jsonify

api_blueprint = Blueprint('mass_flask_api', __name__, template_folder='templates', static_folder='static')

api_blueprint.config = {
    'OBJECTS_PER_PAGE': 100,
    'API_PREFIX': '/api'
}

api_blueprint.apispec = APISpec(
    title='MASS API',
    version='1.0',
    description='RESTful API to the MASS server.',
    plugins=[
        'apispec.ext.marshmallow',
    ],
)


@api_blueprint.route('/swagger/')
def swagger():
    return jsonify(api_blueprint.apispec.to_dict())
