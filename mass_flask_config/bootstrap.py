import os
from flask import redirect, url_for

from mass_flask_api.config import api_blueprint
from mass_flask_webui.config import webui_blueprint
from mass_flask_scheduling.config import scheduling_blueprint
from mass_flask_config.app import app
from mass_flask_core.signals import connect_signals

ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mass_angular_webui')


# @app.route('/webui/', methods=['GET'])
# def webui_proxy():
#     return send_from_directory(ui_path, 'index.html', cache_timeout=0)
#
#
# @app.route('/webui/<path:path>', methods=['GET'])
# def static_proxy(path):
#     if os.path.isfile(os.path.join(ui_path, path)):
#         return send_from_directory(ui_path, path, cache_timeout=0)
#     else:
#         return send_from_directory(ui_path, 'index.html', cache_timeout=0)


@app.route('/version/', methods=['GET'])
def get_version():
    return app.version


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('mass_flask_webui.index'))


def bootstrap_mass_flask():
    connect_signals()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(webui_blueprint, url_prefix='/webui')
    app.register_blueprint(scheduling_blueprint, url_prefix='/scheduling')



