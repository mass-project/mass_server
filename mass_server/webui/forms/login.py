from flask import flash
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

from mass_server.core.models import User


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, extra_validators=None):
        if not super(LoginForm, self).validate():
            return False
        user = User.user_loader(username=self.data['username'], password=self.data['password'])
        if not user:
            flash('Username/password incorrect.', 'warning')
            return False
        else:
            self.user = user
            return True
