from mass_server.api.schemas import SampleRelationSchema, DroppedBySampleRelationSchema, ResolvedBySampleRelationSchema, ContactedBySampleRelationSchema, RetrievedBySampleRelationSchema, SsdeepSampleRelationSchema
from mass_server.api.schemas import SampleSchema, FileSampleSchema, ExecutableBinarySampleSchema, \
    IPSampleSchema, DomainSampleSchema, URISampleSchema


class SchemaMapping:
    @staticmethod
    def get_schema_for_model_class(model_class_name):
        model_conversion = {
                'Sample': SampleSchema,
                'FileSample': FileSampleSchema,
                'ExecutableBinarySample': ExecutableBinarySampleSchema,
                'IPSample': IPSampleSchema,
                'DomainSample': DomainSampleSchema,
                'URISample': URISampleSchema,
                'SampleRelation': SampleRelationSchema,
                'DroppedBySampleRelation': DroppedBySampleRelationSchema,
                'ResolvedBySampleRelation': ResolvedBySampleRelationSchema,
                'ContactedBySampleRelation': ContactedBySampleRelationSchema,
                'RetrievedBySampleRelation': RetrievedBySampleRelationSchema,
                'SsdeepSampleRelation': SsdeepSampleRelationSchema,
                }
        if model_class_name in model_conversion:
            return model_conversion[model_class_name]
        else:
            raise ValueError('Unsupported model type: {}'.format(model_class_name))
