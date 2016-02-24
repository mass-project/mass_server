from mixer.backend.mongoengine import mixer
from mass_flask_core.models import AnalysisSystem, Sample, AnalysisRequest
from mass_flask_core.tests import FlaskTestCase


class AnalysisRequestTestCase(FlaskTestCase):
    def test_is_repr_and_str_correct(self):
        system = mixer.blend(AnalysisSystem, identifier_name='RequestTestSystem')
        sample = mixer.blend(Sample, id='55c863b79b65210a5625411a')
        obj = mixer.blend(AnalysisRequest, sample=sample, analysis_system=system)
        obj.save()
        self.assertEqual(obj.__repr__(), '[AnalysisRequest] 55c863b79b65210a5625411a on RequestTestSystem')
        self.assertEqual(obj.__str__(), '[AnalysisRequest] 55c863b79b65210a5625411a on RequestTestSystem')
