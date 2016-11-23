from flask import flash, render_template, redirect, url_for
from flask_modular_auth import current_authenticated_entity, privilege_required, RolePrivilege

from mass_flask_config.app import app
from mass_flask_webui.config import webui_blueprint
from mass_flask_webui.forms.login import LoginForm


@webui_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if current_authenticated_entity.is_authenticated:
        return redirect(url_for('.profile'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            app.session_provider.login_entity(form.user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('.profile'))
        return render_template('login.html', form=form)


@webui_blueprint.route('/logout/', methods=['GET'])
@privilege_required(RolePrivilege('user'))
def logout():
    app.session_provider.logout_entity()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('mass_flask_webui.index'))
