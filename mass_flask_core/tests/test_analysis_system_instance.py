import datetime
from mixer.backend.mongoengine import mixer
from mongoengine import NotUniqueError, ValidationError
from mass_flask_core.models import AnalysisSystem, AnalysisSystemInstance
from mass_flask_core.tests import FlaskTestCase
from mass_flask_core.utils import TimeFunctions


class AnalysisSystemInstanceTestCase(FlaskTestCase):
    def test_is_repr_and_str_correct(self):
        system = mixer.blend(AnalysisSystem, identifier_name='InstanceTestSystem')
        instance = mixer.blend(AnalysisSystemInstance, uuid='e25b2339-23d4-4544-8c99-f2968a935319', analysis_system=system)
        self.assertEqual(instance.__repr__(), '[AnalysisSystemInstance] InstanceTestSystem e25b2339-23d4-4544-8c99-f2968a935319')
        self.assertEqual(instance.__str__(), '[AnalysisSystemInstance] InstanceTestSystem e25b2339-23d4-4544-8c99-f2968a935319')

    def test_is_uuid_unique(self):
        system = mixer.blend(AnalysisSystem, identifier_name='InstanceTestSystem')
        mixer.blend(AnalysisSystemInstance, uuid='e25b2339-23d4-4544-8c99-f2968a935319', analysis_system=system)
        # Create another system with the same name, expect that it fails
        with self.assertRaises(NotUniqueError):
            mixer.blend(AnalysisSystemInstance, uuid='e25b2339-23d4-4544-8c99-f2968a935319', analysis_system=system)

    def test_is_null_name_forbidden(self):
        with self.assertRaises(ValidationError):
            AnalysisSystemInstance.objects.create(uuid=None)

    def test_is_online_interval_working(self):
        obj = AnalysisSystemInstance()
        obj.last_seen = TimeFunctions.get_timestamp()
        self.assertTrue(obj.is_online)
        obj2 = AnalysisSystemInstance()
        obj2.last_seen = TimeFunctions.get_timestamp() - datetime.timedelta(minutes=10)
        self.assertFalse(obj2.is_online)

    def test_is_update_last_seen_working(self):
        system = mixer.blend(AnalysisSystem, identifier_name='InstanceTestSystem')
        obj = mixer.blend(AnalysisSystemInstance, uuid='e25b2339-23d4-4544-8c99-f2968a935319', analysis_system=system)
        obj.last_seen = TimeFunctions.get_timestamp() - datetime.timedelta(minutes=1)
        obj.save()
        self.assertFalse(TimeFunctions.get_timestamp() - obj.last_seen < datetime.timedelta(seconds=1))
        obj.update_last_seen()
        self.assertTrue(TimeFunctions.get_timestamp() - obj.last_seen < datetime.timedelta(seconds=1))
