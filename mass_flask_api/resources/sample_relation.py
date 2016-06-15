from .base import BaseResource
from flask import request
from flask import jsonify
from mass_flask_api.config import api_blueprint
from mass_flask_core.models import SampleRelation
from mass_flask_api.schemas import SampleRelationSchema
from mass_flask_api.schemas import DroppedBySampleRelationSchema
from mass_flask_api.schemas import ResolvedBySampleRelationSchema
from mass_flask_api.schemas import ContactedBySampleRelationSchema
from mass_flask_api.schemas import RetrievedBySampleRelationSchema
from mass_flask_api.utils import get_pagination_compatible_schema
from mass_flask_api.utils import register_api_endpoint
from mass_flask_core.models import DroppedBySampleRelation
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_schema_for_model_class(model_class_name):
    model_conversion = {
            'SampleRelation': SampleRelationSchema,
            'DroppedBySampleRelation': DroppedBySampleRelationSchema,
            'ResolvedBySampleRelation': ResolvedBySampleRelationSchema,
            'ContactedBySampleRelation': ContactedBySampleRelationSchema,
            'RetrievedBySampleRelation': RetrievedBySampleRelationSchema,
            }
    if model_class_name in model_conversion:
        return model_conversion[model_class_name]
    else:
        raise ValueError('Unsupported model type: {}'.format(model_class_name))


class SampleRelationResource(BaseResource):
    schema = SampleRelationSchema()
    pagination_schema = get_pagination_compatible_schema(SampleRelationSchema)
    model = SampleRelation
    query_key_field = 'id'
    filter_parameters = []

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all sample relations.
            responses:
                200:
                    description: A list of sample relations is returned.
                    schema: SampleRelationSchema
        """
        serialized_sample_relations = []
        paginated_sample_relations = self._get_list()
        logger.error('Got the paginated list')
        for sample_relation in paginated_sample_relations['results']:
            schema = _get_schema_for_model_class(sample_relation.__class__.__name__)
            logger.error('Got next sample_relation {}'.format(sample_relation))
            logger.error('{}'.format(schema().dump(sample_relation)))
            serialized_sample_relations.append(schema().dump(sample_relation).data)
        return jsonify({
            'results': serialized_sample_relations,
            'next': paginated_sample_relations['next'],
            'previous': paginated_sample_relations['previous']
        })

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single sample relation object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The sample relation is returned.
                    schema: SampleRelationSchema
                404:
                    description: No sample relation with the specified id has been found.
        """
        logger.warn('Got to get_detail')
        sample_relation = self.model.objects(id=kwargs['id']).first()
        if not sample_relation:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
        else:
            schema = _get_schema_for_model_class(sample_relation.__class__.__name__)
            return jsonify(schema().dump(sample_relation).data)

    def post(self):
        return jsonify({'error': 'Posting sample relations directly to the sample relation endpoint is not allowed. Instead please use the respective endpoints of each specific relation type.'}), 400

    def put(self, **kwargs):
        return jsonify({'error': 'Updating relation objects via the API is not supported yet.'}), 400

    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing relation object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                204:
                    description: The object has been deleted.
                400:
                    description: The server was not able to delete an object based on the request data.
                404:
                    description: No relation with the specified id has been found.
        """
        return super(SampleRelationResource, self).delete(**kwargs)

    def submit_dropped_by_sample_relation(self):
        """
        ---
        post:
            description: Submit a sample relation between a file and a sample to the MASS server
            parameters:
                - in: body
                  name: body
                  type: DroppedBySampleRelationSchema
            responses:
                201:
                    description: The relation has been uploaded to the MASS server. The metadata of the sample is returned.
                    schema: DroppedBySampleRelationSchema
                400:
                    description: The request is malformed.
        """
        data = request.get_json()
        sample_relation = self.schema.load(data).data
        sample_relation.save()
        schema = _get_schema_for_model_class(sample_relation.__class__.__name__)
        return jsonify(schema().dump(sample_relation).data), 201

#     def submit_ip(self):
#         """
#         ---
#         post:
#             description: Submit an IP address to the MASS server
#             parameters:
#                 - in: body
#                   name: body
#                   type: string
#             responses:
#                 201:
#                     description: The IP address sample has been created on the MASS server. The metadata of the sample is returned.
#                     schema: IPSampleSchema
#                 400:
#                     description: No IP address has been given or the request is malformed.
#         """
#         json_data = request.get_json()
#         if not json_data:
#             return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
#         else:
#             sample = IPSample.create_or_update(**json_data)
#             sample.save()
#             schema = _get_schema_for_model_class(sample.__class__.__name__)
#             return jsonify(schema().dump(sample).data), 201

#     def submit_domain(self):
#         """
#         ---
#         post:
#             description: Submit a domain name to the MASS server
#             parameters:
#                 - in: body
#                   name: body
#                   type: string
#             responses:
#                 201:
#                     description: The domain name sample has been created on the MASS server. The metadata of the sample is returned.
#                     schema: DomainSampleSchema
#                 400:
#                     description: No domain name has been given or the request is malformed.
#         """
#         json_data = request.get_json()
#         if not json_data:
#             return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
#         else:
#             sample = DomainSample.create_or_update(**json_data)
#             sample.save()
#             schema = _get_schema_for_model_class(sample.__class__.__name__)
#             return jsonify(schema().dump(sample).data), 201

#     def submit_uri(self):
#         """
#         ---
#         post:
#             description: Submit a URI to the MASS server
#             parameters:
#                 - in: body
#                   name: body
#                   type: string
#             responses:
#                 201:
#                     description: The URI sample has been created on the MASS server. The metadata of the sample is returned.
#                     schema: URISampleSchema
#                 400:
#                     description: No URI has been given or the request is malformed.
#         """
#         json_data = request.get_json()
#         if not json_data:
#             return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
#         else:
#             sample = URISample.create_or_update(**json_data)
#             sample.save()
#             schema = _get_schema_for_model_class(sample.__class__.__name__)
#             return jsonify(schema().dump(sample).data), 201

#     def reports(self, **kwargs):
#         """
#         ---
#         get:
#             description: Get the reports associated to the given sample
#             parameters:
#                 - in: path
#                   name: id
#                   type: string
#             responses:
#                 200:
#                     description: The list of reports is returned.
#                     schema: ReportSchema
#                 404:
#                     description: No sample with the specified id has been found.
#         """
#         sample = self.model.objects(id=kwargs['id']).first()
#         if not sample:
#             return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
#         else:
#             reports = Report.objects(sample=sample)
#             serialized_result = ReportSchema(many=True).dump(reports)
#             return jsonify({
#                 'results': serialized_result.data,
#             })


register_api_endpoint('sample_relation', SampleRelationResource)

# api_blueprint.add_url_rule('/sample/<id>/download/', view_func=SampleResource().download_file, methods=['GET'], endpoint='sample_download')
# api_blueprint.apispec.add_path(path='/sample/{id}/download/', view=SampleResource.download_file)

api_blueprint.add_url_rule('/sample_relation/submit_dropped_by/', view_func=SampleRelationResource().submit_dropped_by_sample_relation, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample_relation/submit_dropped_by/', view=SampleRelationResource.submit_dropped_by_sample_relation)

# api_blueprint.add_url_rule('/sample/submit_ip/', view_func=SampleResource().submit_ip, methods=['POST'])
# api_blueprint.apispec.add_path(path='/sample/submit_ip/', view=SampleResource.submit_ip)

# api_blueprint.add_url_rule('/sample/submit_domain/', view_func=SampleResource().submit_domain, methods=['POST'])
# api_blueprint.apispec.add_path(path='/sample/submit_domain/', view=SampleResource.submit_domain)

# api_blueprint.add_url_rule('/sample/submit_uri/', view_func=SampleResource().submit_uri, methods=['POST'])
# api_blueprint.apispec.add_path(path='/sample/submit_uri/', view=SampleResource.submit_uri)

# api_blueprint.add_url_rule('/sample/<id>/reports/', view_func=SampleResource().reports, methods=['GET'], endpoint='sample_reports')
# api_blueprint.apispec.add_path(path='/sample/{id}/reports/', view=SampleResource.reports)
