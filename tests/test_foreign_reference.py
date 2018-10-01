from flask import url_for
from mixer.backend.mongoengine import mixer

from mass_server.api.schemas import SampleRelationSchema
from mass_server.core.models import Sample, SampleRelationType
from tests import FlaskTestCase


class SchemaTestCase(FlaskTestCase):
    def test_foreign_reference_sample_relation(self):
        sample1 = mixer.blend(Sample)
        sample1.save()
        sample2 = mixer.blend(Sample)
        sample2.save()
        relation_type = mixer.blend(SampleRelationType, name='test')
        relation_type.save()
        input_data = {
            'sample': url_for('api.sample_namespace_element_get', id=sample1.id, _external=True),
            'other': url_for('api.sample_namespace_element_get', id=sample2.id, _external=True),
            'relation_type': url_for('api.sample_relation_type_namespace_element_get', name=relation_type.name, _external=True)
        }
        with self.app.test_request_context(url_for('api.sample_relation_namespace_collection_get')):
            schema = SampleRelationSchema().load(input_data)
            if schema.errors:
                self.fail('Schema validation failed!' + str(schema.errors))
            relation = schema.data
            self.assertEqual(relation.sample, sample1)
            self.assertEqual(relation.other, sample2)
