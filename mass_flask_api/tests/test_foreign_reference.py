from flask import url_for
from mixer.backend.mongoengine import mixer

from mass_flask_api.schemas import AnalysisSystemInstanceSchema, SampleRelationSchema
from mass_flask_core.models import AnalysisSystem, Sample
from mass_flask_core.tests import FlaskTestCase


class SchemaTestCase(FlaskTestCase):
    def test_foreign_reference_analysis_system(self):
        system = mixer.blend(AnalysisSystem, identifier_name='testsystem')
        system.save()
        input_data = {
            'analysis_system': url_for('mass_flask_api.analysis_system', identifier_name='testsystem', _external=True),
            'uuid': '9e1502c8-56ad-4ffd-bc03-caa34cb6c768'
        }
        schema = AnalysisSystemInstanceSchema().load(input_data)
        if schema.errors:
            self.fail('Schema validation failed!')
        instance = schema.data
        self.assertEqual(instance.analysis_system, system)
        self.assertEqual(instance.uuid, input_data['uuid'])

    def test_foreign_reference_sample_relation(self):
        sample1 = mixer.blend(Sample)
        sample1.save()
        sample2 = mixer.blend(Sample)
        sample2.save()
        input_data = {
            'sample': url_for('mass_flask_api.sample', id=sample1.id, _external=True),
            'other': url_for('mass_flask_api.sample', id=sample2.id, _external=True)
        }
        schema = SampleRelationSchema().load(input_data)
        if schema.errors:
            self.fail('Schema validation failed!')
        relation = schema.data
        print(relation)
        self.assertEqual(relation.sample, sample1)
        self.assertEqual(relation.other, sample2)
