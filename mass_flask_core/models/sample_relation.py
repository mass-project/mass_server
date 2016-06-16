from mongoengine import FloatField
from mongoengine import ReferenceField
from mongoengine import ValidationError
from mass_flask_config.app import db
from .sample import Sample

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class SampleRelation(db.Document):
    sample = ReferenceField(Sample, required=True)
    other = ReferenceField(Sample, required=True)
    meta = {
           'allow_inheritance': True,
           }

    def __repr__(self):
        repr_string = '[{}] {} -- {}'
        return repr_string.format(self.__class__.__name__, self.sample, self.other)

    def __str__(self):
        return self.__repr__()

    def _initialize(self, **kwargs):
        self.sample = Sample.objects(id=kwargs['sample']).first()
        self.other = Sample.objects(id=kwargs['other']).first()

    @property
    def title(self):
        return self.id

    @classmethod
    def create(cls, **kwargs):
        if 'sample' not in kwargs or 'other' not in kwargs:
            raise ValidationError('Parameter "sample" or "other" missing')
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
