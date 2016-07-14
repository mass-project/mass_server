from flask import render_template
from flask.ext.login import login_required, current_user

from mass_flask_core.models import UserAPIKey
from mass_flask_webui.config import webui_blueprint


@webui_blueprint.route('/profile/', methods=['GET'])
@login_required
def profile():
    api_key = UserAPIKey.get_or_create(current_user).generate_auth_token()
    return render_template('profile.html', api_key=api_key)
