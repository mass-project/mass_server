from flask import Blueprint

webui_blueprint = Blueprint('webui', __name__, template_folder='templates', static_folder='static')
