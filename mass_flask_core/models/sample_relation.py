from mongoengine import FloatField
from mongoengine import StringField
from mongoengine import ReferenceField
from mass_flask_config.app import db
from .sample import Sample


class BaseSampleRelation(db.Document):
    sample = ReferenceField(Sample, required=True)
    other = ReferenceField(Sample, required=True)
    meta = {
           'allow_inheritance': True,
           }

    def __repr__(self):
        raise NotImplementedError('This methods needs to be implemented by a concrete SampleRelation type')

    def __str__(self):
        return self.__repr__()


class SampleRelation(BaseSampleRelation):
    SAMPLE_RELATION_TYPES = (
        ('is_dropped_by', 'File was dropped by sample.'),
        ('is_resolved_by', 'Domain is resolved by sample.'),
        ('is_contacted_by', 'IP address is contacted by sample.'),
        ('is_retrieved_by', 'HTTP(S) URL is retrieved by sample.')
    )

    relation_type = StringField(choices=SAMPLE_RELATION_TYPES, required=True)

    def __repr__(self):
        return '[SampleRelation] ' + self.relation_type + ' ' + str(self.sample)


class SsdeepSampleRelation(BaseSampleRelation):
    match = FloatField(min_value=0, max_value=100)

    def __repr__(self):
        repr_string = '[SsdeepSampleRelation] {0.sample} {0.other} => {0.match}'.format(self)
        return repr_string
