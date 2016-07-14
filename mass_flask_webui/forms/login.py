from flask.ext.wtf import Form
from mongoengine import DoesNotExist
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError

from mass_flask_core.models import User


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
        try:
            user = User.objects.get(username=self.data['username'])
        except DoesNotExist:
            self.username.errors.append('Username invalid')
            return False
        if not user.check_password(self.data['password']):
            self.password.errors.append('Password invalid')
            return False
        self.user = user
        return True
