from mixer.backend.mongoengine import mixer
from mongoengine import DoesNotExist

from mass_server.core.models import AnalysisSystem, AnalysisRequest, Sample
from .flask_test_case import FlaskTestCase


class RequestDispatchTestCase(FlaskTestCase):
    def test_are_requests_correct_after_sample_creation(self):
        system = mixer.blend(
            AnalysisSystem, tag_filter_expression='test-a')
        sample_a = mixer.blend(Sample, tags=['test-a'])
        sample_b = mixer.blend(Sample, tags=['test-b'])

        self._are_requests_correct(sample_a, sample_b, system)

    def test_are_requests_correct_after_analysis_system_creation(self):
        sample_a = mixer.blend(Sample, tags=['test-a'])
        sample_b = mixer.blend(Sample, tags=['test-b'])
        system = mixer.blend(
            AnalysisSystem, tag_filter_expression='test-a')

        # Refresh samples from DB, to reload the dispatched_to field
        sample_a.reload()
        sample_b.reload()

        self._are_requests_correct(sample_a, sample_b, system)

    def _are_requests_correct(self, sample_a, sample_b, system):
        self.assertEqual(sample_a.dispatched_to, [system])
        self.assertEqual(sample_b.dispatched_to, [])

        AnalysisRequest.objects.get(sample=sample_a, analysis_system=system)
        with self.assertRaises(DoesNotExist):
            AnalysisRequest.objects.get(
                sample=sample_b, analysis_system=system)
