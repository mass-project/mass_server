from mongoengine import FloatField
from mongoengine import ReferenceField
from mass_flask_config.app import db
from .sample import Sample


class SampleRelation(db.Document):
    sample = ReferenceField(Sample, required=True)
    other = ReferenceField(Sample, required=True)
    meta = {
           'allow_inheritance': True,
           }

    def __repr__(self):
        return '[SampleRelation] ' + ' ' + str(self.sample) + ' -- ' + str(self.other)

    def __str__(self):
        return self.__repr__()


class SsdeepSampleRelation(db.Document):
    match = FloatField(min_value=0, max_value=100)
    sample = ReferenceField(Sample, required=True)
    other = ReferenceField(Sample, required=True)

    def __repr__(self):
        return '[SsdeepSampleRelation]' + ' ' + str(self.sample) + ' ' + \
            str(self.other) + ' => ' + str(self.match)


#    SAMPLE_RELATION_TYPES = (
#        ('is_dropped_by', 'File was dropped by sample.'),
#        ('is_resolved_by', 'Domain is resolved by sample.'),
#        ('is_contacted_by', 'IP address is contacted by sample.'),
#        ('is_retrieved_by', 'HTTP(S) URL is retrieved by sample.')
#    )
