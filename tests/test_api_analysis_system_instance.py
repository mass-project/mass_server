from mixer.backend.mongoengine import mixer

from mass_server.core.models import AnalysisSystem, AnalysisSystemInstance

from .api_test_case import APITestCase


class AnalysisSystemInstanceAPITestCase(APITestCase):
    def test_get_analysis_system_instance_collection(self):
        system = mixer.blend(AnalysisSystem)
        instance = mixer.blend(AnalysisSystemInstance, analysis_system=system)
        self._test_collection('/api/analysis_system_instance/', instance)

    def test_get_analysis_system_instance(self):
        system = mixer.blend(AnalysisSystem)
        instance = mixer.blend(AnalysisSystemInstance, analysis_system=system)
        api_url = '/api/analysis_system_instance/{}/'.format(instance.uuid)
        self._test_element(api_url, instance)

    def test_delete_analysis_system_instance(self):
        system = mixer.blend(AnalysisSystem)
        instance = mixer.blend(AnalysisSystemInstance, analysis_system=system)
        api_url = '/api/analysis_system_instance/{}/'.format(instance.uuid)
        self._test_delete(api_url)

    def test_add_analysis_system_instance(self):
        system = mixer.blend(AnalysisSystem, identifier_name='test')
        data = {
            'analysis_system': 'http://localhost/api/analysis_system/test/',
            'uuid': '4d8e5234-0a13-4e5a-a804-7bb56a5f25c4'
        }
        api_url = '/api/analysis_system_instance/'
        self._test_post(api_url, data)
