from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField, FormField, DateField, IntegerField, FloatField
from wtforms.validators import Length, Optional, NumberRange, IPAddress


class NoCSRFForm(Form):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(NoCSRFForm, self).__init__(*args, **kwargs)


class CommonSearchForm(NoCSRFForm):
    delivery_date__lte = DateField('Delivered before', validators=[Optional()], description='<i>Enter like this: YYYY-MM-DD</i>')
    delivery_date__gte = DateField('Delivered after', validators=[Optional()], description='<i>Enter like this: YYYY-MM-DD</i>')
    first_seen_date__lte = DateField('First seen before', validators=[Optional()], description='<i>Enter like this: YYYY-MM-DD</i>')
    first_seen_date__gte = DateField('First seen after', validators=[Optional()], description='<i>Enter like this: YYYY-MM-DD</i>')
    tags = TextAreaField('Sample tags', validators=[Optional(), Length(min=4)], description='<i>One tag per line - Examples: filetype:windows-binary, packerfamily:upx</i>')


class FileSampleSearchForm(NoCSRFForm):
    md5sum = StringField('MD5 hash', validators=[Optional(), Length(min=32, max=32)])
    sha1sum = StringField('SHA1 hash', validators=[Optional(), Length(min=40, max=40)])
    sha256sum = StringField('SHA256 hash', validators=[Optional(), Length(min=64, max=64)])
    sha512sum = StringField('SHA512 hash', validators=[Optional(), Length(min=128, max=128)])
    mime_type = StringField('Mime type', validators=[Optional(), Length(min=4)], description='<i>Examples: application/x-dosexec, text/xml</i>')
    file_names = StringField('File name', validators=[Optional(), Length(min=4)])
    file_size__lte = IntegerField('File size smaller than', validators=[Optional()], description='Enter file size in number of bytes')
    file_size__gte = IntegerField('File size larger than', validators=[Optional()], description='Enter file size in number of bytes')
    shannon_entropy__lte = FloatField('Shannon entropy smaller than', validators=[Optional(), NumberRange(min=0, max=8)], description='Enter floating point value between 0 and 8')
    shannon_entropy__gte = FloatField('Shannon entropy larger than', validators=[Optional(), NumberRange(min=0, max=8)], description='Enter floating point value between 0 and 8')


class IPSampleSearchForm(NoCSRFForm):
    ip_address = StringField('IP address', validators=[Optional(), IPAddress()])


class DomainSampleSearchForm(NoCSRFForm):
    domain = StringField('Domain is exactly', validators=[Optional(), Length(min=4)])
    domain__contains = StringField('Domain contains', validators=[Optional(), Length(min=4)])
    domain__startswith = StringField('Domain starts with', validators=[Optional(), Length(min=4)])
    domain__endswith = StringField('Domain ends with', validators=[Optional(), Length(min=4)])


class URISampleSearchForm(NoCSRFForm):
    uri = StringField('URI is exactly', validators=[Optional(), Length(min=4)])
    uri__contains = StringField('URI contains', validators=[Optional(), Length(min=4)])
    uri__startswith = StringField('URI starts with', validators=[Optional(), Length(min=4)])
    uri__endswith = StringField('URI ends with', validators=[Optional(), Length(min=4)])


class SampleSearchForm(NoCSRFForm):
    common = FormField(CommonSearchForm, label='Common search filters')
    file = FormField(FileSampleSearchForm, label='Search filters related to file samples')
    ip = FormField(IPSampleSearchForm, label='Search filters related to IP samples')
    domain = FormField(DomainSampleSearchForm, label='Search filters related to domain samples')
    uri = FormField(URISampleSearchForm, label='Search filters related to URI samples')
    submit = SubmitField()
