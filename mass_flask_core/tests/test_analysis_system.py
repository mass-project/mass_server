from mass_flask_core.models import AnalysisSystem
from mongoengine.errors import ValidationError, NotUniqueError
from mass_flask_core.tests.flask_test_case import FlaskTestCase
from mixer.backend.mongoengine import mixer


class AnalysisSystemTestCase(FlaskTestCase):
    def test_is_repr_and_str_correct(self):
        obj = mixer.blend(AnalysisSystem, identifier_name='Test')
        self.assertEqual(obj.__repr__(), '[AnalysisSystem] Test')
        self.assertEqual(obj.__str__(), '[AnalysisSystem] Test')

    def test_is_system_name_unique(self):
        with self.assertRaises(NotUniqueError):
            a1 = mixer.blend(AnalysisSystem, identifier_name='duplicate')
            a1.save()
            a2 = mixer.blend(AnalysisSystem, identifier_name='duplicate')
            a2.save()

    def test_is_null_name_forbidden(self):
        with self.assertRaises(ValidationError):
            mixer.blend(AnalysisSystem, identifier_name=None)

    def test_is_empty_name_forbidden(self):
        with self.assertRaises(ValidationError):
            mixer.blend(AnalysisSystem, identifier_name='')

    def test_is_short_name_forbidden(self):
        with self.assertRaises(ValidationError):
            mixer.blend(AnalysisSystem, identifier_name='aa')
