from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, IPAddress, URL

from mass_flask_core.models import TLPLevelField

class FileSampleSubmitForm(Form):
    file = FileField('File', validators=[FileRequired()])
    tlp_level = SelectField('Sample privacy (TLP level)', coerce=int, choices=[
        (TLPLevelField.TLP_LEVEL_WHITE, 'WHITE (unlimited)'),
        (TLPLevelField.TLP_LEVEL_GREEN, 'GREEN (community)'),
        (TLPLevelField.TLP_LEVEL_AMBER, 'AMBER (limited distribution)'),
        (TLPLevelField.TLP_LEVEL_RED, 'RED (personal for named recipients)'),
    ])
    submit = SubmitField()


class IPSampleSubmitForm(Form):
    ip_address = StringField('IPv4/IPv6 address', validators=[InputRequired(), IPAddress()])
    tlp_level = SelectField('Sample privacy (TLP level)', coerce=int, choices=[
        (TLPLevelField.TLP_LEVEL_WHITE, 'WHITE (unlimited)'),
        (TLPLevelField.TLP_LEVEL_GREEN, 'GREEN (community)'),
        (TLPLevelField.TLP_LEVEL_AMBER, 'AMBER (limited distribution)'),
        (TLPLevelField.TLP_LEVEL_RED, 'RED (personal for named recipients)'),
    ])
    submit = SubmitField()


class DomainSampleSubmitForm(Form):
    domain = StringField('Domain name', validators=[InputRequired()])
    tlp_level = SelectField('Sample privacy (TLP level)', coerce=int, choices=[
        (TLPLevelField.TLP_LEVEL_WHITE, 'WHITE (unlimited)'),
        (TLPLevelField.TLP_LEVEL_GREEN, 'GREEN (community)'),
        (TLPLevelField.TLP_LEVEL_AMBER, 'AMBER (limited distribution)'),
        (TLPLevelField.TLP_LEVEL_RED, 'RED (personal for named recipients)'),
    ])
    submit = SubmitField()


class URISampleSubmitForm(Form):
    uri = StringField('URI', validators=[InputRequired(), URL()])
    tlp_level = SelectField('Sample privacy (TLP level)', coerce=int, choices=[
        (TLPLevelField.TLP_LEVEL_WHITE, 'WHITE (unlimited)'),
        (TLPLevelField.TLP_LEVEL_GREEN, 'GREEN (community)'),
        (TLPLevelField.TLP_LEVEL_AMBER, 'AMBER (limited distribution)'),
        (TLPLevelField.TLP_LEVEL_RED, 'RED (personal for named recipients)'),
    ])
    submit = SubmitField()
