from flask_modular_auth import current_authenticated_entity
from flask_mongoengine import BaseQuerySet
from mongoengine import StringField, DateTimeField, ListField, ReferenceField, EmbeddedDocumentField, FileField, IntField, FloatField, EmbeddedDocument, ValidationError, DoesNotExist, Q, GenericReferenceField

from mass_server.core.utils import TimeFunctions, HashFunctions, FileFunctions, ListFunctions, StringFunctions
from mass_server import db
from .analysis_system import AnalysisSystem
from .comment import CommentsMixin
from .tag import TagsMixin
from .tlp_level import TLPLevelMixin


class FileFeatureDocument(EmbeddedDocument):
    file = FileField()
    file_names = ListField(StringField())
    file_size = IntField(required=True)
    magic_string = StringField(required=True)
    mime_type = StringField(required=True)
    md5sum = StringField(min_length=32, max_length=32, required=True)
    sha1sum = StringField(min_length=40, max_length=40, required=True)
    sha256sum = StringField(min_length=64, max_length=64, required=True)
    sha512sum = StringField(min_length=128, max_length=128, required=True)
    ssdeep_hash = StringField(max_length=200, required=True)
    shannon_entropy = FloatField(min_value=0, max_value=8, required=True)


class UniqueSampleFeaturesDocument(EmbeddedDocument):
    file = EmbeddedDocumentField(FileFeatureDocument)
    ipv4 = StringField(regex=r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
    ipv6 = StringField(regex=r'([0-9a-f]{1,4}:{0,2}){1,8}')
    port = IntField()
    domain = StringField()
    uri = StringField(regex=r'\w+://.*')
    custom_unique_feature = StringField()


class SampleQuerySet(BaseQuerySet):
    def get_with_tlp_level_filter(self):
        if current_authenticated_entity.is_authenticated:
            return self.filter(
                Q(tlp_level__lte=current_authenticated_entity.max_tlp_level) |
                Q(created_by=current_authenticated_entity._get_current_object(
                )))
        else:
            return self.filter(
                tlp_level__lte=current_authenticated_entity.max_tlp_level)


class Sample(db.Document, CommentsMixin, TagsMixin, TLPLevelMixin):
    delivery_dates = ListField(
        DateTimeField(default=TimeFunctions.get_timestamp, required=True))
    first_seen = DateTimeField(
        default=TimeFunctions.get_timestamp, required=True)
    dispatched_to = ListField(ReferenceField(AnalysisSystem))
    created_by = GenericReferenceField()
    unique_features = EmbeddedDocumentField(UniqueSampleFeaturesDocument)

    meta = {
        'ordering': ['-first_seen'],
        'indexes': ['first_seen'],
        'queryset_class': SampleQuerySet
    }

    def __repr__(self):
        return '[{}] {}'.format(str(self.__class__.__name__), str(self.id))

    def __str__(self):
        return self.__repr__()

    def add_tags(self, tags):
        self.tags = ListFunctions.merge_lists_without_duplicates(
            self.tags, tags)
        self.save()

    def _update_delivery_dates(self):
        self.delivery_dates.append(TimeFunctions.get_timestamp())

    def _update_first_seen(self, **kwargs):
        if 'first_seen' in kwargs:
            self.first_seen = kwargs['first_seen']

    def update(self, **kwargs):
        self._update_tags(**kwargs)
        self._update_tlp_level(**kwargs)
        self._update_first_seen(**kwargs)
        self._update_delivery_dates()

    @classmethod
    def create_or_update(cls, **kwargs):
        if 'unique_features' not in kwargs:
            raise ValueError('unique_features parameter is missing.')
        unique_features = kwargs['unique_features']
        unique_filter = {}
        if 'file' in unique_features:
            file = unique_features['file']
            hash_values = HashFunctions.get_hash_values_dictionary(file)
            unique_filter['unique_features__file__sha512sum'] = hash_values[
                'sha512sum']
        if 'ipv4' in unique_features:
            unique_filter['unique_features__ipv4'] = unique_features['ipv4']
        if 'ipv6' in unique_features:
            unique_filter['unique_features__ipv6'] = unique_features['ipv6']
        if 'port' in unique_features:
            unique_filter['unique_features__port'] = unique_features['port']
        if 'domain' in unique_features:
            unique_filter['unique_features__domain'] = unique_features[
                'domain']
        if 'uri' in unique_features:
            unique_filter['unique_features__uri'] = unique_features['uri']
        if 'custom_unique_feature' in unique_features:
            unique_filter[
                'unique_features__custom_unique_feature'] = unique_features[
                    'custom_unique_feature']

        if len(unique_filter) == 0:
            raise ValidationError('No unique features provided.')

        try:
            sample = cls.objects.get(**unique_filter)
        except DoesNotExist:
            sample = Sample.create(unique_features)
        sample.update(**kwargs)
        sample.save()
        return sample

    @classmethod
    def create(cls, unique_features):
        sample = Sample()
        sample.unique_features = UniqueSampleFeaturesDocument()
        sample.delivery_dates = []

        if current_authenticated_entity.is_authenticated:
            sample.created_by = current_authenticated_entity._get_current_object(
            )

        if 'file' in unique_features:
            file = unique_features['file']
            sample.unique_features.file = FileFeatureDocument()
            sample.unique_features.file.md5sum = HashFunctions.md5_hash(file)
            sample.unique_features.file.sha1sum = HashFunctions.sha1_hash(file)
            sample.unique_features.file.sha256sum = HashFunctions.sha256_hash(
                file)
            sample.unique_features.file.sha512sum = HashFunctions.sha512_hash(
                file)
            sample.unique_features.file.ssdeep_hash = HashFunctions.ssdeep_hash(
                file)
            sample.unique_features.file.shannon_entropy = HashFunctions.shannon_entropy(
                file)
            sample.unique_features.file.file_size = FileFunctions.get_file_size(
                file)
            sample.unique_features.file.mime_type = FileFunctions.get_mime_type_from_file(
                file)
            sample.unique_features.file.magic_string = FileFunctions.get_magic_string_from_file(
                file)
            file_name = FileFunctions.get_file_name(file)
            sample.unique_features.file.file.put(
                file,
                filename=file_name,
                content_type=sample.unique_features.file.mime_type)
            sample.unique_features.file.file_names = [file_name]
            file_extension = FileFunctions.get_file_extension(file_name)
            sample.tags = FileFunctions.assemble_tag_list(
                sample.unique_features.file.magic_string,
                sample.unique_features.file.mime_type, file_extension)

        if 'ipv4' in unique_features:
            sample.unique_features.ipv4 = unique_features['ipv4']

        if 'ipv6' in unique_features:
            sample.unique_features.ipv6 = unique_features['ipv6']

        if 'port' in unique_features:
            sample.unique_features.port = unique_features['port']

        if 'domain' in unique_features:
            sample.unique_features.domain = unique_features['domain']

        if 'uri' in unique_features:
            sample.unique_features.uri = unique_features['uri']

        if 'custom_unique_feature' in unique_features:
            sample.unique_features.custom_unique_feature = unique_features[
                'custom_unique_feature']

        sample.save()
        return sample
