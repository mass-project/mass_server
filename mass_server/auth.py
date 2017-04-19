from flask import flash, redirect, url_for, request
from flask_modular_auth import AuthManager, current_authenticated_entity


def unauthorized_callback():
    if current_authenticated_entity.is_authenticated:
        flash('You are not authorized to access this resource!', 'warning')
        return redirect(url_for('webui.index'))
    else:
        return redirect(url_for('webui.login', next=request.url))


auth = AuthManager(unauthorized_callback=unauthorized_callback)