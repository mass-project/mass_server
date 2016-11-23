from flask import render_template
from flask_modular_auth import current_authenticated_entity, privilege_required, RolePrivilege

from mass_flask_core.models import UserAPIKey
from mass_flask_webui.config import webui_blueprint


@webui_blueprint.route('/profile/', methods=['GET'])
@privilege_required(RolePrivilege('user'))
def profile():
    api_key = UserAPIKey.get_or_create(current_authenticated_entity).generate_auth_token()
    return render_template('profile.html', api_key=api_key)
