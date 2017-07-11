from mongoengine import FloatField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import ReferenceField
from mongoengine import DictField
from mongoengine import ListField
from mongoengine import ValidationError
from mass_flask_config.app import db
from .sample import Sample

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class SampleRelationType(db.Document):
    name = StringField(min_length=3, max_length=64, unique=True, required=True)
    directed = BooleanField(required=True)
    description = StringField(default='')

    meta = {
            'ordering': ['name'],
            'indexes': ['name'],
            }

    def __repr__(self):
        repr_string = '[{}] {} ({})'
        return repr_string.format(self.__class__.__name__, self.name, self.directed)

    def __str__(self):
        return self.__repr__()


class SampleRelation(db.Document):
    sample = ReferenceField(Sample, required=True)
    other = ReferenceField(Sample, required=True)
    relation_type = ReferenceField(SampleRelationType, required=True)
    tags = ListField(StringField())
    additional_metadata = DictField()
    meta = {
        'allow_inheritance': True,
    }

    def __repr__(self):
        repr_string = '[{}({})] {} -- {}'
        return repr_string.format(self.__class__.__name__, self.relation_type.name, self.sample, self.other)

    def __str__(self):
        return self.__repr__()

    def _initialize(self, **kwargs):
        self.sample = Sample.objects(id=kwargs['sample']).first()
        self.other = Sample.objects(id=kwargs['other']).first()
        self.relation_type = SampleRelationType.objects(id=kwargs['name']).first()

    @property
    def title(self):
        return self.id

    @classmethod
    def create(cls, **kwargs):
        if 'sample' not in kwargs or 'other' not in kwargs or 'relation_type' not in kwargs:
            raise ValidationError('At least one of the parameters "sample", "other", "relation_type" is missing')
        else:
            sample_relation = cls()
            sample_relation._initialize(**kwargs)
            sample_relation.save()
            return sample_relation


class DroppedBySampleRelation(SampleRelation):
    '''
    Relation between a file and a sample. The file was somehow dropped by or extracted from the sample.

    Attributes:
        sample  The file wich was dropped.
        other   The sample which dropped the file.
    '''

    def __repr__(self):
        repr_string = '[DroppedBySampleRelation] {} was dropped by {}'
        return repr_string.format(self.sample, self.other)


class ResolvedBySampleRelation(SampleRelation):
    '''
    Relation between a domain and a sample, i.e. the domain was resolved by the sample.

    Attributes:
        sample  the domain
        other   The sample which resolved the domain.
    '''

    def __repr__(self):
        repr_string = '[ResolvedBySampleRelation] {} was resolved by {}'
        return repr_string.format(self.sample, self.other)


class ContactedBySampleRelation(SampleRelation):
    '''
    Relation between an IP address and a sample, i.e. the IP was contacted by the sample.

    Attributes:
        sample  the IP address
        other   The sample which contacted the IP.
    '''

    def __repr__(self):
        repr_string = '[ContactedBySampleRelation] {} was contacted by {}'
        return repr_string.format(self.sample, self.other)


class RetrievedBySampleRelation(SampleRelation):
    '''
    Relation between an HTTP(S) URL  and a sample, i.e. the URL was retrieved by the sample.

    Attributes:
        sample  the IP address
        other   The sample which contacted the IP.
    '''

    def __repr__(self):
        repr_string = '[RetrievedBySampleRelation] {} was retrieved by {}'
        return repr_string.format(self.sample, self.other)


class SsdeepSampleRelation(SampleRelation):
    match = FloatField(min_value=0, max_value=100, required=True)

    def __repr__(self):
        repr_string = '[SsdeepSampleRelation] {0.sample} {0.other} => {0.match}'.format(self)
        return repr_string
