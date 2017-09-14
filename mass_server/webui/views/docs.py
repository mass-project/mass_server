from flask import render_template
from mass_server.webui.config import webui_blueprint

@webui_blueprint.route('/docs')
def docs():
    return render_template('docs.html')
