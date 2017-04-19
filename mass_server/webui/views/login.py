from flask import flash, render_template, redirect, url_for, current_app
from flask_modular_auth import current_authenticated_entity, privilege_required, RolePrivilege

from mass_server.webui.config import webui_blueprint
from mass_server.webui.forms import LoginForm


@webui_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if current_authenticated_entity.is_authenticated:
        return redirect(url_for('.profile'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            current_app.session_provider.login_entity(form.user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('.profile'))
        return render_template('login.html', form=form)


@webui_blueprint.route('/logout/', methods=['GET'])
@privilege_required(RolePrivilege('user'))
def logout():
    current_app.session_provider.logout_entity()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('webui.index'))
