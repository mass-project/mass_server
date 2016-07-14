from flask import flash, render_template, redirect, url_for
from flask.ext.login import login_user, login_required, logout_user

from mass_flask_webui.config import webui_blueprint
from mass_flask_webui.forms.login import LoginForm


@webui_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash('Logged in successfully!', 'success')
    return render_template('login.html', form=form)


@webui_blueprint.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('mass_flask_webui.index'))
