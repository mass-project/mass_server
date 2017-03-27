from mixer.backend.mongoengine import mixer
from mongoengine import ValidationError

from mass_server.core.models import Sample, FileSample, TLPLevelField
from mass_server.core.utils import TimeFunctions
from tests import FlaskTestCase


class SampleTestCase(FlaskTestCase):
    def setUp(self):
        self._timestamp = TimeFunctions.get_timestamp()

    def _create_file_sample(self):
        file_sample_args = {
            'file': open('tests/test_data/gpl-2.0.txt', 'rb'),
            'comment': 'GPL 2.0',
            'long_comment': 'This is a copy of the GPL for testing.',
            'first_seen': self._timestamp,
            'tlp_level': TLPLevelField.TLP_LEVEL_WHITE
        }
        file_sample = FileSample.create_or_update(**file_sample_args)
        return file_sample

    def test_is_repr_and_str_correct(self):
        sample = mixer.blend(Sample, id='55c863b79b65210a5625411a')
        self.assertEqual(sample.__repr__(), '[Sample] 55c863b79b65210a5625411a')
        self.assertEqual(sample.__str__(), '[Sample] 55c863b79b65210a5625411a')

    def test_sample_can_not_be_created_directly(self):
        kwargs = {}
        with self.assertRaises(ValidationError):
            Sample.create_or_update(**kwargs)

    def test_is_comment_correct(self):
        sample = mixer.blend(Sample, comment='Some comment')
        self.assertEqual(sample.comment, 'Some comment')

    def test_is_long_comment_correct(self):
        sample = mixer.blend(Sample, long_comment='Some long comment')
        self.assertEqual(sample.long_comment, 'Some long comment')

    def test_is_file_name_correct(self):
        file_sample = self._create_file_sample()
        self.assertIn('gpl-2.0.txt', file_sample.file_names)

    def test_is_file_size_correct(self):
        file_sample = self._create_file_sample()
        self.assertEqual(file_sample.file_size, 18092)

    def test_is_md5sum_correct(self):
        file_sample = self._create_file_sample()
        self.assertEqual(file_sample.md5sum, 'b234ee4d69f5fce4486a80fdaf4a4263')

    def test_is_sha1sum_correct(self):
        file_sample = self._create_file_sample()
        self.assertEqual(file_sample.sha1sum, '4cc77b90af91e615a64ae04893fdffa7939db84c')

    def test_is_sha256sum_correct(self):
        file_sample = self._create_file_sample()
        self.assertEqual(file_sample.sha256sum, '8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643')

    def test_is_sha512sum_correct(self):
        file_sample = self._create_file_sample()
        self.assertEqual(file_sample.sha512sum, 'aee80b1f9f7f4a8a00dcf6e6ce6c41988dcaedc4de19d9d04460cbfb05d99829ffe8f9d038468eabbfba4d65b38e8dbef5ecf5eb8a1b891d9839cda6c48ee957')

    def test_is_ssdeep_hash_correct(self):
        file_sample = self._create_file_sample()
        self.assertEqual(file_sample.ssdeep_hash, '384:ghUwi5rpL676yV12rPd34ZomzM2FR+dWF7jUI:gmFWixMFzMdm7jUI')

    def test_is_shannon_entropy_correct(self):
        file_sample = self._create_file_sample()
        self.assertAlmostEqual(file_sample.shannon_entropy, 4.666564742606159)

    def test_is_first_seen_correct(self):
        file_sample = self._create_file_sample()
        self.assertEquals(file_sample.first_seen, self._timestamp)

    def test_file_sample_can_not_be_created_without_file(self):
        kwargs = {}
        with self.assertRaises(ValidationError):
            FileSample.create_or_update(**kwargs)

    def test_is_sample_type_tag_present(self):
        file_sample = self._create_file_sample()
        self.assertIn('sample-type:filesample', file_sample.tags)

    def test_is_invalid_tag_rejected(self):
        invalid_tags = [
            'tag with spaces',
            'some:weird/§&$-chars'
        ]
        for tag in invalid_tags:
            self.assertInvalidTag(tag)

    def test_is_valid_tag_accepted(self):
        valid_tags = [
            'foo:bar',
            'bar:foo/test',
            'some-thing:special',
            'withoutspecialcharacters',
            'some_dashes-included',
            'tag:withnumber1234'
        ]
        for tag in valid_tags:
            self.assertValidTag(tag)

    def assertInvalidTag(self, tag):
        with self.assertRaises(ValidationError):
            sample = mixer.blend(Sample, tags=[tag])

    def assertValidTag(self, tag):
        try:
            mixer.blend(Sample, tags=[tag])
        except ValidationError:
            self.fail('Validation of a valid tag failed!')

    # def test_ip_sample_can_not_be_created_without_ip(self):
    #     kwargs = {}
    #     with self.assertRaises(ValidationError):
    #         IPSample.create_or_update(**kwargs)
    #
    # def test_is_ip_address_correct(self):
    #     self.assertEquals(self.ip_sample.ip_address, '127.0.0.1')
