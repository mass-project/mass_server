from flask.ext.marshmallow.fields import URLFor
from marshmallow.fields import List, String

from mass_flask_api.config import api_blueprint
from .base import BaseSchema, ForeignReferenceField
from mass_flask_core.models import Sample, FileSample, ExecutableBinarySample, AnalysisSystem, IPSample, DomainSample, URISample


class SampleSchema(BaseSchema):
    url = URLFor('.sample', id='<id>', _external=True)
    dispatched_to = List(ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name'))

    class Meta(BaseSchema.Meta):
        model = Sample
        dump_only = [
            'id',
            'dispatched_to',
            '_cls',
            'delivery_date'
        ]

api_blueprint.apispec.definition('Sample', schema=SampleSchema)


class FileSampleSchema(SampleSchema):
    url = URLFor('.sample', id='<id>', _external=True)
    dispatched_to = List(ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name'))
    file = URLFor('.sample_download', id='<id>', _external=True)

    class Meta(BaseSchema.Meta):
        model = FileSample
        dump_only = SampleSchema.Meta.dump_only + [
            'file_size',
            'file_names',
            'magic_string',
            'md5sum',
            'sha1sum',
            'sha256sum',
            'sha512sum',
            'shannon_entropy',
            'ssdeep_hash'
        ]

api_blueprint.apispec.definition('FileSample', schema=FileSampleSchema)


class ExecutableBinarySampleSchema(FileSampleSchema):
    url = URLFor('.sample', id='<id>', _external=True)
    dispatched_to = List(ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name'))
    # dispatched_to = List(String)

    class Meta(BaseSchema.Meta):
        model = ExecutableBinarySample
        dump_only = FileSampleSchema.Meta.dump_only + [
            'filesystem_events',
            'registry_events',
            'sections',
            'resources',
            'imports',
            'strings'
        ]

api_blueprint.apispec.definition('ExecutableBinarySample', schema=ExecutableBinarySampleSchema)


class IPSampleSchema(SampleSchema):
    url = URLFor('.sample', id='<id>', _external=True)
    dispatched_to = List(ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name'))

    class Meta(BaseSchema.Meta):
        model = IPSample
        dump_only = SampleSchema.Meta.dump_only

api_blueprint.apispec.definition('IPSample', schema=IPSampleSchema)


class DomainSampleSchema(SampleSchema):
    url = URLFor('.sample', id='<id>', _external=True)
    dispatched_to = List(ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name'))

    class Meta(BaseSchema.Meta):
        model = DomainSample
        dump_only = SampleSchema.Meta.dump_only

api_blueprint.apispec.definition('DomainSample', schema=DomainSampleSchema)


class URISampleSchema(SampleSchema):
    url = URLFor('.sample', id='<id>', _external=True)
    dispatched_to = List(ForeignReferenceField(endpoint='mass_flask_api.analysis_system', queryset=AnalysisSystem.objects(), query_parameter='identifier_name'))

    class Meta(BaseSchema.Meta):
        model = URISample
        dump_only = SampleSchema.Meta.dump_only

api_blueprint.apispec.definition('URISample', schema=URISampleSchema)
