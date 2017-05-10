from mixer.backend.mongoengine import mixer
from mongoengine import DoesNotExist

from mass_flask_core.models import AnalysisSystem, AnalysisRequest, IPSample, URISample
from mass_flask_core.tests import FlaskTestCase


class RequestDispatchTestCase(FlaskTestCase):
    def test_are_requests_correct_after_sample_creation(self):
        system = mixer.blend(AnalysisSystem, tag_filter_expression='sample-type:ipsample')
        ipsample = mixer.blend(IPSample, tags=['sample-type:ipsample'])
        urisample = mixer.blend(URISample, tags=['sample-type:urisample'])

        self._are_requests_correct(ipsample, urisample, system)

    def test_are_requests_correct_after_analysis_system_creation(self):
        ipsample = mixer.blend(IPSample, tags=['sample-type:ipsample'])
        urisample = mixer.blend(URISample, tags=['sample-type:urisample'])
        system = mixer.blend(AnalysisSystem, tag_filter_expression='sample-type:ipsample')

        # Refresh samples from DB, to reload the dispatched_to field
        ipsample = IPSample.objects.get(id=ipsample.id)
        urisample = URISample.objects.get(id=urisample.id)

        self._are_requests_correct(ipsample, urisample, system)

    def _are_requests_correct(self, ipsample, urisample, system):
        self.assertEqual(ipsample.dispatched_to, [system])
        self.assertEqual(urisample.dispatched_to, [])

        AnalysisRequest.objects.get(sample=ipsample, analysis_system=system)
        with self.assertRaises(DoesNotExist):
            AnalysisRequest.objects.get(sample=urisample, analysis_system=system)