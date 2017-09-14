from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import Optional, Regexp

from mass_server.core.models import TLPLevelField


class SampleSubmitForm(Form):
    file = FileField('File')
    ipv4 = StringField('IPv4 address', validators=[Optional(), Regexp(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')])
    ipv6 = StringField('IPv6 address', validators=[Optional(), Regexp(r'([0-9a-f]{1,4}:{0,2}){1,8}')])
    port = IntegerField('Port', validators=[Optional()])
    domain = StringField('Domain name')
    uri = StringField('URI', validators=[Optional(), Regexp(r'\w+://.*')])
    custom_unique_feature = StringField('Custom unique feature')
    tlp_level = SelectField('Sample privacy (TLP level)', coerce=int, choices=[
        (TLPLevelField.TLP_LEVEL_WHITE, 'WHITE (unlimited)'),
        (TLPLevelField.TLP_LEVEL_GREEN, 'GREEN (community)'),
        (TLPLevelField.TLP_LEVEL_AMBER, 'AMBER (limited distribution)'),
        (TLPLevelField.TLP_LEVEL_RED, 'RED (personal for named recipients)'),
    ])
    submit = SubmitField()
