from mongoengine import EmbeddedDocument, StringField, ReferenceField


class SampleRelation(EmbeddedDocument):
    SAMPLE_RELATION_TYPES = (
        ('is_dropped_by', 'File was dropped by sample.'),
        ('is_resolved_by', 'Domain is resolved by sample.'),
        ('is_contacted_by', 'IP address is contacted by sample.'),
        ('is_retrieved_by', 'HTTP(S) URL is retrieved by sample.')
    )

    sample = ReferenceField('Sample', required=True)
    relation_type = StringField(choices=SAMPLE_RELATION_TYPES, required=True)

    def __repr__(self):
        return '[SampleRelation] ' + self.relation_type + ' ' + str(self.sample)

    def __str__(self):
        return self.__repr__()
