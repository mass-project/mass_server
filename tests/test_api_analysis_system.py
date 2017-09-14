from mixer.backend.mongoengine import mixer

from mass_server.core.models import AnalysisSystem

from .api_test_case import APITestCase


class AnalysisSystemAPITestCase(APITestCase):
    def test_get_analysis_system_collection(self):
        self._test_collection('/api/analysis_system/',
                              mixer.blend(AnalysisSystem))

    def test_get_analysis_system(self):
        obj = mixer.blend(AnalysisSystem)
        api_url = '/api/analysis_system/{}/'.format(obj.identifier_name)
        self._test_element(api_url, obj)

    def test_patch_analysis_system(self):
        obj = mixer.blend(AnalysisSystem)
        patch = {'verbose_name': 'patched system'}
        api_url = '/api/analysis_system/{}/'.format(obj.identifier_name)
        self._test_patch(api_url, obj, patch)

    def test_delete_analysis_system(self):
        obj = mixer.blend(AnalysisSystem)
        api_url = '/api/analysis_system/{}/'.format(obj.identifier_name)
        self._test_delete(api_url)

    def test_add_analysis_system(self):
        data = {
            'identifier_name': 'test',
            'verbose_name': 'Test system',
            'information_text': 'Just for testing'
        }
        api_url = '/api/analysis_system/'
        self._test_post(api_url, data)
        
