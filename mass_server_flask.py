import os
from flask import send_from_directory

from mass_flask_config import app
from mass_flask_api.config import api_blueprint
from mass_flask_core.signals import connect_signals


@app.route('/')
def hello_world():
    return 'Hello World!'


ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mass_angular_webui")


@app.route('/webui/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(ui_path, path)


if __name__ == '__main__':
    connect_signals()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.run()
