import json
from mixer.backend.mongoengine import mixer

from mass_server.core.models import User, UserLevel, UserAPIKey

from .flask_test_case import FlaskTestCase

class APITestCase(FlaskTestCase):
    def _get_headers(self):
        user = mixer.blend(User, user_level=UserLevel.USER_LEVEL_ADMIN)
        user.save()
        key = UserAPIKey.get_or_create(user)
        key.save()
        return {
            'Authorization': 'APIKEY ' + key.generate_auth_token(),
            'Content-Type': 'application/json'
        }

    def _test_collection(self, api_url, obj):
        result = self.client.get(api_url, headers=self._get_headers())
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result_dict['results'][0]['id'], str(obj.id))

    def _test_element(self, api_url, obj):
        result = self.client.get(api_url, headers=self._get_headers())
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result_dict['id'], str(obj.id))

    def _test_patch(self, api_url, obj, patch):
        result = self.client.patch(
            api_url, data=json.dumps(patch), headers=self._get_headers())
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertEqual(result.status_code, 200)
        for key in patch:
            self.assertEqual(patch[key], result_dict[key])

    def _test_delete(self, api_url):
        result = self.client.delete(
            api_url,
            headers=self._get_headers())
        self.assertEqual(result.status_code, 204)

    def _test_post(self, api_url, data):
        result = self.client.post(
            api_url,
            data=json.dumps(data),
            headers=self._get_headers())
        result_dict = json.loads(result.data.decode('utf-8'))
        self.assertEqual(result.status_code, 201)
        for key in data:
            self.assertEqual(data[key], result_dict[key])
