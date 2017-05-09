from mixer.backend.mongoengine import mixer
from mongoengine import DoesNotExist

from mass_flask_core.models import AnalysisSystem, AnalysisRequest, IPSample, URISample
from mass_flask_core.tests import FlaskTestCase


class RequestDispatchTestCase(FlaskTestCase):
    def test_are_requests_correct_after_sample_creation(self):
        system = mixer.blend(AnalysisSystem, tag_filter_expression='sample-type:ipsample')
        ipsample = mixer.blend(IPSample, tags=['sample-type:ipsample'])
        urisample = mixer.blend(URISample, tags=['sample-type:urisample'])

        self.assertEqual(ipsample.dispatched_to, [system])
        self.assertEqual(urisample.dispatched_to, [])

        AnalysisRequest.objects.get(sample=ipsample, analysis_system=system)
        with self.assertRaises(DoesNotExist):
            AnalysisRequest.objects.get(sample=urisample, analysis_system=system)
