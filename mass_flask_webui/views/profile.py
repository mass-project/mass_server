from flask import redirect, render_template, url_for, flash
from flask_modular_auth import current_authenticated_entity, privilege_required, RolePrivilege

from mass_flask_core.models import UserAPIKey
from mass_flask_webui.config import webui_blueprint
from mass_flask_webui.forms.password import PasswordForm
from mass_flask_webui.forms.profile import ProfileForm


@webui_blueprint.route('/profile/', methods=['GET'])
@privilege_required(RolePrivilege('user'))
def profile():
    api_key = UserAPIKey.get_or_create(current_authenticated_entity).generate_auth_token()
    return render_template('profile.html', api_key=api_key, user=current_authenticated_entity)


@webui_blueprint.route('/profile/edit/', methods=['GET', 'POST'])
@privilege_required(RolePrivilege('user'))
def profile_edit():
    user = current_authenticated_entity
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'organization': user.organization,
        'email': user.email
    }
    form = ProfileForm(**initial_data)
    if form.validate_on_submit():
        user.first_name = form.data['first_name']
        user.last_name = form.data['last_name']
        user.organization = form.data['organization']
        user.email = form.data['email']
        user.save()
        flash('Personal information has been changed.', 'success')
        return redirect(url_for('mass_flask_webui.profile'))
    else:
        return render_template('profile_edit.html', form=form)


@webui_blueprint.route('/profile/change_password/', methods=['GET', 'POST'])
@privilege_required(RolePrivilege('user'))
def profile_change_password():
    user = current_authenticated_entity
    form = PasswordForm()
    if form.validate_on_submit():
        user.set_password(form.data['password'])
        user.save()
        flash('Password has been changed.', 'success')
        return redirect(url_for('mass_flask_webui.profile'))
    else:
        return render_template('password.html', form=form)