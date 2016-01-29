from apispec import APISpec
from flask import request, jsonify
from flask.views import MethodView

from mass_flask_config import app
from mass_flask_api.config import api_blueprint
from mass_flask_core.signals import connect_signals


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    connect_signals()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.run()
