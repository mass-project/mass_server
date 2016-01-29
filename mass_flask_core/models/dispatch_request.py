from mass_flask_config import db
from mongoengine import DateTimeField, ReferenceField, IntField
from .sample import Sample
from mass_flask_core.utils import TimeFunctions


class DispatchRequest(db.Document):
    sample = ReferenceField(Sample, required=True)
    dispatch_requested = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    priority = IntField(default=0, required=True)

    meta = {
        'ordering': ['-dispatch_requested'],
        'indexes': ['dispatch_requested']
    }

    def __repr__(self):
        return '[DispatchRequest] {}'.format(self.sample.comment)

    def __str__(self):
        return self.__repr__()
