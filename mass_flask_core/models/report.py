from mass_flask_config import db
from mongoengine import StringField, DateTimeField, ReferenceField, IntField, ListField
from .analysis_system import AnalysisSystem
from .sample import Sample
from mass_flask_core.utils import TimeFunctions


class Report(db.DynamicDocument):

    REPORT_STATUS_CODE_OK = 0
    REPORT_STATUS_CODE_FAILURE = 1

    REPORT_STATUS_CODES = (
        (REPORT_STATUS_CODE_OK, 'OK'),
        (REPORT_STATUS_CODE_FAILURE, 'FAIL'),
    )

    analysis_system = ReferenceField(AnalysisSystem, required=True)
    sample = ReferenceField(Sample, required=True)
    report_date = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    status = IntField(choices=REPORT_STATUS_CODES, default=REPORT_STATUS_CODE_OK, required=True)
    tags = ListField(StringField())
    # is_malware = BooleanField(default=False, required=True)
    # short_result = StringField(max_length=400)
    # tags = models.ManyToManyField(Tag)

    meta = {
        'ordering': ['-report_date'],
        'indexes': ['report_date']
    }

    def __repr__(self):
        return '[Report] {} on {}'.format(self.sample.id, self.analysis_system.identifier_name)

    def __str__(self):
        return self.__repr__()
