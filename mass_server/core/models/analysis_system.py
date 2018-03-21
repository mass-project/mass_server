from mongoengine import StringField, ListField, IntField

from mass_server import db


class AnalysisSystem(db.Document):
    identifier_name = StringField(min_length=3, max_length=50, unique=True, required=True)
    verbose_name = StringField(max_length=200, required=True)
    information_text = StringField(required=False)
    tag_filter_expression = StringField(max_length=400, required=True, default='')
    time_schedule = ListField(IntField(), default=[0])

    filter_parameters = {
        'identifier_name': None,
        'verbose_name': None,
        'identifier_name__contains': None,
        'verbose_name__contains': None
    }

    meta = {
        'ordering': ['identifier_name'],
        'indexes': ['identifier_name']
    }

    def __repr__(self):
        return '[AnalysisSystem] {}'.format(self.identifier_name)

    def __str__(self):
        return self.__repr__()
