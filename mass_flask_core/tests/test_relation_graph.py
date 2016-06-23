from mixer.backend.mongoengine import mixer

from mass_flask_core.models import Sample, SampleRelation
from mass_flask_core.tests import FlaskTestCase
from mass_flask_core.utils import GraphFunctions


class RelationGraphTestCase(FlaskTestCase):
    def test_simple_graph(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        mixer.blend(SampleRelation, sample=sample1, other=sample2)
        self.assertEqual(GraphFunctions.get_relation_graph(sample1), {(sample1.to_dbref(), sample2.to_dbref(), 'SampleRelation')})

    def test_transitive_graph(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        sample3 = mixer.blend(Sample)
        mixer.blend(SampleRelation, sample=sample1, other=sample2)
        mixer.blend(SampleRelation, sample=sample2, other=sample3)
        self.assertEqual(GraphFunctions.get_relation_graph(sample1), {
            (sample1.to_dbref(), sample2.to_dbref(), 'SampleRelation'),
            (sample2.to_dbref(), sample3.to_dbref(), 'SampleRelation')
        })

    def test_depth_parameter(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        sample3 = mixer.blend(Sample)
        mixer.blend(SampleRelation, sample=sample1, other=sample2)
        mixer.blend(SampleRelation, sample=sample2, other=sample3)
        self.assertEqual(GraphFunctions.get_relation_graph(sample1, depth=1), {(sample1.to_dbref(), sample2.to_dbref(), 'SampleRelation')})

    def test_triangle(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        sample3 = mixer.blend(Sample)
        mixer.blend(SampleRelation, sample=sample1, other=sample2)
        mixer.blend(SampleRelation, sample=sample2, other=sample3)
        mixer.blend(SampleRelation, sample=sample3, other=sample1)
        self.assertEqual(GraphFunctions.get_relation_graph(sample1), {
            (sample1.to_dbref(), sample2.to_dbref(), 'SampleRelation'),
            (sample2.to_dbref(), sample3.to_dbref(), 'SampleRelation'),
            (sample3.to_dbref(), sample1.to_dbref(), 'SampleRelation')
        })
