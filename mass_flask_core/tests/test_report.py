from mass_flask_core.models import AnalysisSystem, Report, Sample
from mixer.backend.mongoengine import mixer
from mass_flask_core.tests import FlaskTestCase


class ReportTestCase(FlaskTestCase):

    def test_is_repr_and_str_correct(self):
        system = mixer.blend(AnalysisSystem, identifier_name='ReportTestSystem')
        sample = mixer.blend(Sample, id='55cdd8e89b65211708b7da46')
        obj = mixer.blend(Report, sample=sample, analysis_system=system)
        self.assertEqual(obj.__repr__(), '[Report] 55cdd8e89b65211708b7da46 on ReportTestSystem')
        self.assertEqual(obj.__str__(), '[Report] 55cdd8e89b65211708b7da46 on ReportTestSystem')
