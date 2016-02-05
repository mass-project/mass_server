import os
from flask import send_from_directory
from mass_flask_api.config import api_blueprint
from mass_flask_config import app
from mass_flask_core.signals import connect_signals

ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mass_angular_webui')


@app.route('/webui/', methods=['GET'])
def webui_proxy():
    return send_from_directory(ui_path, 'index.html', cache_timeout=0)


@app.route('/webui/<path:path>', methods=['GET'])
def static_proxy(path):
    if os.path.isfile(os.path.join(ui_path, path)):
        return send_from_directory(ui_path, path, cache_timeout=0)
    else:
        return send_from_directory(ui_path, 'index.html', cache_timeout=0)


def bootstrap_mass_flask():
    connect_signals()
    app.register_blueprint(api_blueprint, url_prefix='/api')
