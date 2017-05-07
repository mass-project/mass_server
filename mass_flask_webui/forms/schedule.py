from flask_wtf import Form
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import InputRequired


class ScheduleForm(Form):
    analysis_system = SelectField('Analysis system', choices=[], validators=[InputRequired()])
    priority = IntegerField('Priority', validators=[InputRequired()], default=0)
    submit = SubmitField('Schedule')
