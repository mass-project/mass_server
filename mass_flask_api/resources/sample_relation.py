from flask import jsonify
from flask import request

from mass_flask_api.config import api_blueprint
from mass_flask_api.schemas import SampleRelationSchema, DroppedBySampleRelationSchema, ResolvedBySampleRelationSchema, ContactedBySampleRelationSchema, RetrievedBySampleRelationSchema, SsdeepSampleRelationSchema
from mass_flask_api.schemas import SchemaMapping
from mass_flask_api.utils import get_pagination_compatible_schema, check_api_key
from mass_flask_api.utils import register_api_endpoint
from mass_flask_core.models import SampleRelation, AdminPrivilege
from .base import BaseResource



class SampleRelationResource(BaseResource):
    schema = SampleRelationSchema()
    pagination_schema = get_pagination_compatible_schema(SampleRelationSchema)
    model = SampleRelation
    query_key_field = 'id'
    filter_parameters = []

    @check_api_key()
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
        for sample_relation in paginated_sample_relations['results']:
            schema = SchemaMapping.get_schema_for_model_class(sample_relation.__class__.__name__)
            serialized_sample_relations.append(schema().dump(sample_relation).data)
        return jsonify({
            'results': serialized_sample_relations,
            'next': paginated_sample_relations['next'],
            'previous': paginated_sample_relations['previous']
        })

    @check_api_key()
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
        sample_relation = self.model.objects(id=kwargs['id']).first()
        if not sample_relation:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
        else:
            schema = SchemaMapping.get_schema_for_model_class(sample_relation.__class__.__name__)
            return jsonify(schema().dump(sample_relation).data)

    def post(self):
        return jsonify({'error': 'Posting sample relations directly to the sample relation endpoint is not allowed. Instead please use the respective endpoints of each specific relation type.'}), 400

    def put(self, **kwargs):
        return jsonify({'error': 'Updating relation objects via the API is not supported yet.'}), 400

    @check_api_key(required_privileges=[AdminPrivilege])
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

    @check_api_key()
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
        schema = DroppedBySampleRelationSchema()
        sample_relation = schema.load(data).data
        sample_relation.save()
        return jsonify(schema.dump(sample_relation).data), 201

    @check_api_key()
    def submit_resolved_by_sample_relation(self):
        """
        ---
        post:
            description: Submit a sample relation between a domain and a sample to the MASS server
            parameters:
                - in: body
                  name: body
                  type: ResolvedBySampleRelationSchema
            responses:
                201:
                    description: The relation has been uploaded to the MASS server. The metadata of the sample is returned.
                    schema: ResolvedBySampleRelationSchema
                400:
                    description: The request is malformed.
        """
        data = request.get_json()
        schema = ResolvedBySampleRelationSchema()
        sample_relation = schema.load(data).data
        sample_relation.save()
        return jsonify(schema.dump(sample_relation).data), 201

    @check_api_key()
    def submit_contacted_by_sample_relation(self):
        """
        ---
        post:
            description: Submit a sample relation between an IP and a sample to the MASS server
            parameters:
                - in: body
                  name: body
                  type: ContactedBySampleRelationSchema
            responses:
                201:
                    description: The relation has been uploaded to the MASS server. The metadata of the sample is returned.
                    schema: ContactedBySampleRelationSchema
                400:
                    description: The request is malformed.
        """
        data = request.get_json()
        schema = ContactedBySampleRelationSchema()
        sample_relation = schema.load(data).data
        sample_relation.save()
        return jsonify(schema.dump(sample_relation).data), 201

    @check_api_key()
    def submit_retrieved_by_sample_relation(self):
        """
        ---
        post:
            description: Submit a sample relation between a HTTP(S) URL and a sample to the MASS server
            parameters:
                - in: body
                  name: body
                  type: RetrievedBySampleRelationSchema
            responses:
                201:
                    description: The relation has been uploaded to the MASS server. The metadata of the sample is returned.
                    schema: RetrievedBySampleRelationSchema
                400:
                    description: The request is malformed.
        """
        data = request.get_json()
        schema = RetrievedBySampleRelationSchema()
        sample_relation = schema.load(data).data
        sample_relation.save()
        return jsonify(schema.dump(sample_relation).data), 201

    @check_api_key()
    def submit_ssdeep_sample_relation(self):
        """
        ---
        post:
            description: Submit a sample relation between two sample files.
            parameters:
                - in: body
                  name: body
                  type: SsdeepSampleRelationSchema
            responses:
                201:
                    description: The relation has been uploaded to the MASS server. The metadata of the sample is returned.
                    schema: SsdeepSampleRelationSchema
                400:
                    description: The request is malformed.
        """
        data = request.get_json()
        schema = SsdeepSampleRelationSchema()
        sample_relation = schema.load(data).data
        sample_relation.save()
        return jsonify(self.schema.dump(sample_relation).data), 201


register_api_endpoint('sample_relation', SampleRelationResource)


api_blueprint.add_url_rule('/sample_relation/submit_dropped_by/', view_func=SampleRelationResource().submit_dropped_by_sample_relation, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample_relation/submit_dropped_by/', view=SampleRelationResource.submit_dropped_by_sample_relation)

api_blueprint.add_url_rule('/sample_relation/submit_resolved_by/', view_func=SampleRelationResource().submit_resolved_by_sample_relation, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample_relation/submit_resolved_by/', view=SampleRelationResource.submit_resolved_by_sample_relation)

api_blueprint.add_url_rule('/sample_relation/submit_contacted_by/', view_func=SampleRelationResource().submit_contacted_by_sample_relation, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample_relation/submit_contacted_by/', view=SampleRelationResource.submit_contacted_by_sample_relation)

api_blueprint.add_url_rule('/sample_relation/submit_retrieved_by/', view_func=SampleRelationResource().submit_retrieved_by_sample_relation, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample_relation/submit_retrieved_by/', view=SampleRelationResource.submit_retrieved_by_sample_relation)

api_blueprint.add_url_rule('/sample_relation/submit_ssdeep/', view_func=SampleRelationResource().submit_ssdeep_sample_relation, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample_relation/submit_ssdeep/', view=SampleRelationResource.submit_ssdeep_sample_relation)
