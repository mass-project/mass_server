from flask_wtf import Form
from wtforms import DateTimeField, SelectField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from mass_server.core.models import AnalysisSystem
from datetime import datetime


class RequestAnalysisForm(Form):
    analysis_system = SelectField('Analysis system', choices=[], validators=[InputRequired()])
    priority = IntegerField('Priority', validators=[InputRequired()], default=0)
    schedule_after = DateTimeField('Schedule after (YYYY-MM-DD hh:mm:ss)', default=datetime.now)
    submit = SubmitField('Request')

    def __init__(self):
        super(RequestAnalysisForm, self).__init__()
        self._query_analysis_system_choices()

    def _query_analysis_system_choices(self):
        analysis_systems = []
        for system in AnalysisSystem.objects:
            analysis_systems.append((system.identifier_name, system.verbose_name))

        self.analysis_system.choices = analysis_systems
