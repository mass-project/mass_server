from flask_wtf import Form
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class PasswordForm(Form):
    password = PasswordField('Enter new password', [
            Length(min=2),
            DataRequired(),
            EqualTo('password_confirm', message='Passwords must match')
        ])
    password_confirm = PasswordField('Enter new password again', [DataRequired()])
    submit = SubmitField()
