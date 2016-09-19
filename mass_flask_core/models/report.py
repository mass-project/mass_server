from flask import json

from mass_flask_config.app import db
from mongoengine import StringField, DateTimeField, ReferenceField, IntField, ListField, EmbeddedDocument, FileField, EmbeddedDocumentListField, DictField, MapField, GridFSProxy
from .analysis_system import AnalysisSystem
from .sample import Sample
from mass_flask_core.utils import TimeFunctions


class JSONReportObject(EmbeddedDocument):
    name = StringField(required=True)
    _json_data = FileField()

    def get_as_dict(self):
        return json.loads(self._json_data.read())


class RawReportObject(EmbeddedDocument):
    name = StringField(required=True)
    _raw_data = FileField()

    def get_raw_data(self):
        return self._raw_data.read()


class Report(db.Document):

    REPORT_STATUS_CODE_OK = 0
    REPORT_STATUS_CODE_FAILURE = 1

    REPORT_STATUS_CODES = (
        (REPORT_STATUS_CODE_OK, 'OK'),
        (REPORT_STATUS_CODE_FAILURE, 'FAIL'),
    )

    analysis_system = ReferenceField(AnalysisSystem, required=True)
    sample = ReferenceField(Sample, required=True)
    analysis_date = DateTimeField()
    upload_date = DateTimeField(default=TimeFunctions.get_timestamp, required=True)
    status = IntField(choices=REPORT_STATUS_CODES, default=REPORT_STATUS_CODE_OK, required=True)
    error_message = StringField(null=True, required=False)
    tags = ListField(StringField())
    additional_metadata = DictField()
    json_report_objects = MapField(field=FileField(db_alias='default-mongodb-connection'))
    raw_report_objects = MapField(field=FileField(db_alias='default-mongodb-connection'))

    meta = {
        'ordering': ['-upload_date'],
        'indexes': ['upload_date']
    }

    def __repr__(self):
        return '[Report] {} on {}'.format(self.sample.id, self.analysis_system.identifier_name)

    def __str__(self):
        return self.__repr__()

    def _add_report_object(self, file, target):
        proxy = GridFSProxy(db_alias='default-mongodb-connection')
        proxy.put(file)
        target[file.name] = proxy

    def add_json_report_object(self, file):
        self._add_report_object(file, self.json_report_objects)

    def add_raw_report_object(self, file):
        self._add_report_object(file, self.raw_report_objects)
