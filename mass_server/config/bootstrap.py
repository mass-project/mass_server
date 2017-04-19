import os

from flask import redirect, url_for

from mass_server.api.config import api_blueprint
from mass_server.config.app import app
from mass_server.core.signals import connect_signals
from mass_server.scheduling.config import scheduling_blueprint
from mass_server.webui.config import webui_blueprint

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