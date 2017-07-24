from flask_marshmallow.fields import URLFor
from mass_flask_core.models import SampleRelation
from mass_flask_core.models import SampleRelationType
from mass_flask_core.models import DroppedBySampleRelation
from mass_flask_core.models import ResolvedBySampleRelation
from mass_flask_core.models import ContactedBySampleRelation
from mass_flask_core.models import RetrievedBySampleRelation
from mass_flask_core.models import SsdeepSampleRelation
from mass_flask_core.models import Sample
from mass_flask_api.config import api_blueprint
from .base import BaseSchema
from .base import ForeignReferenceField
from marshmallow.fields import Float


class SampleRelationTypeSchema(BaseSchema):
    url = URLFor('.sample_relation_type_detail', name='<name>', _external=True)

    class Meta(BaseSchema.Meta):
        model = SampleRelationType

api_blueprint.apispec.definition('SampleRelationType', schema=SampleRelationTypeSchema)


class SampleRelationSchema(BaseSchema):
    url = URLFor('.sample_relation_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', queryset=Sample.objects(), query_parameter='id')
    other = ForeignReferenceField(endpoint='.sample_detail', queryset=Sample.objects(), query_parameter='id')
    relation_type = ForeignReferenceField(endpoint='.sample_relation_type_detail', queryset=SampleRelationType.objects(), query_parameter='name')

    class Meta(BaseSchema.Meta):
        model = SampleRelation
        dump_only = [
                'id',
                '_cls'
                ]

api_blueprint.apispec.definition('SampleRelation', schema=SampleRelationSchema)


class DroppedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = DroppedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only

api_blueprint.apispec.definition('DroppedBySampleRelation', schema=DroppedBySampleRelationSchema)


class ResolvedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = ResolvedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only

api_blueprint.apispec.definition('ResolvedBySampleRelation', schema=ResolvedBySampleRelationSchema)


class ContactedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = ContactedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only

api_blueprint.apispec.definition('ContactedBySampleRelation', schema=ContactedBySampleRelationSchema)


class RetrievedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = RetrievedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only

api_blueprint.apispec.definition('RetrievedBySampleRelation', schema=RetrievedBySampleRelationSchema)


class SsdeepSampleRelationSchema(SampleRelationSchema):
    match = Float()

    class Meta(BaseSchema.Meta):
        model = SsdeepSampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only

api_blueprint.apispec.definition('SsdeepSampleRelation', schema=SsdeepSampleRelationSchema)
