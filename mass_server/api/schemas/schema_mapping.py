from .analysis_request import AnalysisRequestSchema
from .analysis_system_instance import AnalysisSystemInstanceSchema
from .analysis_system import AnalysisSystemSchema
from .report import ReportSchema
from .sample_relation import SampleRelationSchema, DroppedBySampleRelationSchema, ResolvedBySampleRelationSchema, ContactedBySampleRelationSchema, RetrievedBySampleRelationSchema, SsdeepSampleRelationSchema
from .sample import SampleSchema
from .scheduled_analysis import ScheduledAnalysisSchema

class SchemaMapping:
    @staticmethod
    def get_schema_for_model_class(model_class_name):
        model_conversion = {
                'AnalysisRequest': AnalysisRequestSchema(),
                'AnalysisSystemInstance': AnalysisSystemInstanceSchema(),
                'AnalysisSystem': AnalysisSystemSchema(),
                'Report': ReportSchema(),
                'Sample': SampleSchema(),
                'SampleRelation': SampleRelationSchema(),
                'DroppedBySampleRelation': DroppedBySampleRelationSchema(),
                'ResolvedBySampleRelation': ResolvedBySampleRelationSchema(),
                'ContactedBySampleRelation': ContactedBySampleRelationSchema(),
                'RetrievedBySampleRelation': RetrievedBySampleRelationSchema(),
                'SsdeepSampleRelation': SsdeepSampleRelationSchema(),
                'ScheduledAnalysis': ScheduledAnalysisSchema()
                }
        if model_class_name in model_conversion:
            return model_conversion[model_class_name]
        else:
            raise ValueError('Unsupported model type: {}'.format(model_class_name))
