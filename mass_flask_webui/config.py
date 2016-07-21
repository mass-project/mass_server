from flask import Blueprint
from flask.ext.login import LoginManager
from mongoengine import DoesNotExist

from mass_flask_core.models import User, AnonymousUser

webui_blueprint = Blueprint('mass_flask_webui', __name__, template_folder='templates', static_folder='static')
login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser


@webui_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except DoesNotExist:
        return None
