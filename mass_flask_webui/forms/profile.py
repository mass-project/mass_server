from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField


class ProfileForm(Form):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    organization = StringField('Organization/Company')
    email = EmailField('Email address')
    submit = SubmitField()