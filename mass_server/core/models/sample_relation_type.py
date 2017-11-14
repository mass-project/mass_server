from mongoengine import BooleanField, StringField
from mass_server import db

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
