from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, FormField
from wtforms.validators import Length, InputRequired, IPAddress, URL


class SubmitOptionalDataForm(Form):
    comment = StringField('Comment', validators=[Length(min=0, max=200)])
    long_comment = StringField('Long comment')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(SubmitOptionalDataForm, self).__init__(*args, **kwargs)


class FileSampleSubmitForm(Form):
    file = FileField('File', validators=[FileRequired()])
    submit = SubmitField()
    optional = FormField(SubmitOptionalDataForm, label='Optional data')


class IPSampleSubmitForm(Form):
    ip_address = StringField('IPv4/IPv6 address', validators=[InputRequired(), IPAddress()])
    submit = SubmitField()
    optional = FormField(SubmitOptionalDataForm, label='Optional data')


class DomainSampleSubmitForm(Form):
    domain = StringField('Domain name', validators=[InputRequired()])
    submit = SubmitField()
    optional = FormField(SubmitOptionalDataForm, label='Optional data')


class URISampleSubmitForm(Form):
    uri = StringField('URI', validators=[InputRequired(), URL()])
    submit = SubmitField()
    optional = FormField(SubmitOptionalDataForm, label='Optional data')
