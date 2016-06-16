from unittest import TestCase
from mongoengine.connection import get_connection
from mass_flask_config.app import app
from mass_flask_config.bootstrap import bootstrap_mass_flask


class FlaskTestCase(TestCase):

    def _clean_test_database(self):
        connection = get_connection()
        connection.drop_database(app.config['MONGODB_SETTINGS']['db'])

    def __call__(self, result=None):
        self._pre_setup()
        super(FlaskTestCase, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        bootstrap_mass_flask()
        if app.config['TESTING'] is False:
            raise RuntimeError('Running unit test without TESTING=True in configuration. Aborting.')
        self.app = app
        self.client = app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()
        self._clean_test_database()

