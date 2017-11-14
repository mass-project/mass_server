from mongoengine import ReferenceField, StringField, ListField, DictField, ValidationError
from mass_server import db
from .sample import Sample
from .sample_relation_type import SampleRelationType


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
