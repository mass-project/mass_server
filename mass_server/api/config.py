from flask import Blueprint, jsonify, url_for, _request_ctx_stack
from flask_slimrest import SlimRest

api_blueprint = Blueprint('api', __name__)
api = SlimRest(api_blueprint)


def api_unauthorized_callback():
    return jsonify({'error': 'You do not have access to this resource.'}), 403


@api_blueprint.before_request
def before_request_set_unauthorized_callback():
    ctx = _request_ctx_stack.top
    ctx.unauthorized_callback = api_unauthorized_callback
    return None
