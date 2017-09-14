from mongoengine import StringField, ListField
from mass_server.core.utils import ListFunctions

class TagsMixin:
    tags = ListField(StringField(regex=r'^[\w:\-\_\/\+\.]+$'))

    def _update_tags(self, **kwargs):
        if 'tags' in kwargs:
            self.tags = ListFunctions.merge_lists_without_duplicates(self.tags, kwargs['tags'])
