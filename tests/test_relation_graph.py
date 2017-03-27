from mixer.backend.mongoengine import mixer

from mass_server.core.models import Sample, SampleRelation
from mass_server.core.utils import GraphFunctions
from tests import FlaskTestCase


class RelationGraphTestCase(FlaskTestCase):
    def assertGraphEqual(self, sample, result_set, depth=None):
        if depth is None:
            self.assertEqual(GraphFunctions.get_relation_graph(sample), result_set)
        else:
            self.assertEqual(GraphFunctions.get_relation_graph(sample, depth=depth), result_set)

    def test_simple_graph(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        rel1 = mixer.blend(SampleRelation, sample=sample1, other=sample2)
        self.assertGraphEqual(sample1, {rel1})

    def test_transitive_graph(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        sample3 = mixer.blend(Sample)
        rel1 = mixer.blend(SampleRelation, sample=sample1, other=sample2)
        rel2 = mixer.blend(SampleRelation, sample=sample2, other=sample3)
        self.assertGraphEqual(sample1, {rel1, rel2})

    def test_depth_parameter(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        sample3 = mixer.blend(Sample)
        rel1 = mixer.blend(SampleRelation, sample=sample1, other=sample2)
        rel2 = mixer.blend(SampleRelation, sample=sample2, other=sample3)
        self.assertGraphEqual(sample1, {rel1}, depth=1)
        self.assertGraphEqual(sample1, {rel1, rel2}, depth=2)

    def test_triangle(self):
        sample1 = mixer.blend(Sample)
        sample2 = mixer.blend(Sample)
        sample3 = mixer.blend(Sample)
        rel1 = mixer.blend(SampleRelation, sample=sample1, other=sample2)
        rel2 = mixer.blend(SampleRelation, sample=sample2, other=sample3)
        rel3 = mixer.blend(SampleRelation, sample=sample3, other=sample1)
        self.assertGraphEqual(sample1, {rel1, rel2, rel3})
