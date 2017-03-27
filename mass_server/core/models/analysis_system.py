from mongoengine import StringField

from mass_server.config.app import db


class AnalysisSystem(db.Document):
    identifier_name = StringField(min_length=3, max_length=50, unique=True, required=True)
    verbose_name = StringField(max_length=200, required=True)
    information_text = StringField()
    tag_filter_expression = StringField(max_length=400, required=True, default='')

    meta = {
        'ordering': ['identifier_name'],
        'indexes': ['identifier_name']
    }

    def __repr__(self):
        return '[AnalysisSystem] {}'.format(self.identifier_name)

    def __str__(self):
        return self.__repr__()
