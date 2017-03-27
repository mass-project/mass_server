from unittest import TestCase

from mongoengine import connection

from mass_server.config.bootstrap import bootstrap_mass_flask
from mass_server.config.app import app


class FlaskTestCase(TestCase):
    @staticmethod
    def _clean_test_database():
        conn = connection.get_connection()
        db = connection.get_db()
        conn.drop_database(db)

    def __call__(self, result=None):
        self._pre_setup()
        super(FlaskTestCase, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        bootstrap_mass_flask()
        if not 'MASS_TESTING' in app.config or app.config['MASS_TESTING'] is False:
            raise RuntimeError('Running unit test without TESTING=True in configuration. Aborting.')
        self.app = app
        self.client = app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()
        self._clean_test_database()

