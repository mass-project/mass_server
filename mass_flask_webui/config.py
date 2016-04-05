from flask import Blueprint

webui_blueprint = Blueprint('mass_flask_webui', __name__, template_folder='templates', static_folder='static')

webui_blueprint.config = {
}


