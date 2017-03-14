from flask import jsonify, request
from mongoengine import DoesNotExist

from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege

from mass_flask_api.config import api_blueprint
from mass_flask_api.schemas import SampleRelationSchema, DroppedBySampleRelationSchema, ResolvedBySampleRelationSchema, ContactedBySampleRelationSchema, RetrievedBySampleRelationSchema, SsdeepSampleRelationSchema
from mass_flask_api.schemas import SchemaMapping
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_core.models import SampleRelation
from .base import BaseResource


class SampleRelationResource(BaseResource):
    schema = SampleRelationSchema()
    pagination_schema = get_pagination_compatible_schema(SampleRelationSchema)
    queryset = SampleRelation.objects
    query_key_field = 'id'
    filter_parameters = []

    @privilege_required(AuthenticatedPrivilege())
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

    @privilege_required(AuthenticatedPrivilege())
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
        try:
            sample_relation = self.queryset.get(id=kwargs['id'])
            schema = SchemaMapping.get_schema_for_model_class(sample_relation.__class__.__name__)
            return jsonify(schema().dump(sample_relation).data)
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404

    def post(self):
        return jsonify({'error': 'Posting sample relations directly to the sample relation endpoint is not allowed. Instead please use the respective endpoints of each specific relation type.'}), 400

    def put(self, **kwargs):
        return jsonify({'error': 'Updating relation objects via the API is not supported yet.'}), 400

    @privilege_required(RolePrivilege('admin'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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

        return jsonify(schema.dump(sample_relation).data), 201


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
