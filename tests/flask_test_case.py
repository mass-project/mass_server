from unittest import TestCase
from mongoengine import connection

from mass_server import get_app


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
        self.app = get_app(debug=True, testing=True)
        if 'TESTING' not in self.app.config or self.app.config['TESTING'] is False:
            raise RuntimeError('Running unit test without TESTING=True in configuration. Aborting.')
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()
        self._clean_test_database()

