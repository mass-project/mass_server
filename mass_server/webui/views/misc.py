from flask import render_template

from mass_server.webui.config import webui_blueprint


@webui_blueprint.route('/apidocs/')
def apidocs():
    return render_template('apidocs.html')


@webui_blueprint.route('/cli_scripts/')
def cli_scripts():
    return render_template('cli_scripts.html')
