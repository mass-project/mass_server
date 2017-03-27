import json

from flask import jsonify, request
from flask_modular_auth import privilege_required, RolePrivilege, AuthenticatedPrivilege
from mongoengine import DoesNotExist

from mass_server.core.utils import GraphFunctions
from mass_server.core.models import Sample, FileSample, Report, IPSample, DomainSample, URISample
from mass_server.api.config import api_blueprint
from mass_server.api.schemas import SampleSchema, ReportSchema, SchemaMapping
from mass_server.api.utils import get_pagination_compatible_schema, register_api_endpoint
from .base import BaseResource


class SampleResource(BaseResource):
    schema = SampleSchema()
    pagination_schema = get_pagination_compatible_schema(SampleSchema)
    queryset = Sample.objects.get_with_tlp_level_filter
    query_key_field = 'id'
    filter_parameters = [
        'md5sum',
        'sha1sum',
        'sha256sum',
        'sha512sum',
        '_cls',
        '_cls__startswith'
    ]

    @privilege_required(AuthenticatedPrivilege())
    def get_list(self):
        """
        ---
        get:
            description: Get a list of all samples.
            parameters:
                - in: query
                  name: md5sum
                  type: string
                - in: query
                  name: sha1sum
                  type: string
                - in: query
                  name: sha256sum
                  type: string
                - in: query
                  name: sha512sum
                  type: string
            responses:
                200:
                    description: A list of samples is returned.
                    schema: SampleSchema
        """
        serialized_samples = []
        paginated_samples = self._get_list()
        for sample in paginated_samples['results']:
            schema = SchemaMapping.get_schema_for_model_class(sample.__class__.__name__)
            serialized_samples.append(schema().dump(sample).data)
        return jsonify({
            'results': serialized_samples,
            'next': paginated_samples['next'],
            'previous': paginated_samples['previous']
        })

    @privilege_required(AuthenticatedPrivilege())
    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single sample object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The sample is returned.
                    schema: SampleSchema
                404:
                    description: No sample with the specified id has been found.
        """
        try:
            sample = self.queryset().get(id=kwargs['id'])
            schema = SchemaMapping.get_schema_for_model_class(sample.__class__.__name__)
            data = schema().dump(sample).data
            return jsonify(data)
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404

    def post(self):
        return jsonify({'error': 'Posting samples directly to the sample endpoint is not allowed. Instead please use the respective endpoints of each specific sample type.'}), 400

    def put(self, **kwargs):
        return jsonify({'error': 'Updating sample objects via the API is not supported yet.'}), 400

    @privilege_required(RolePrivilege('admin'))
    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing sample object
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
                    description: No sample with the specified id has been found.
        """
        return super(SampleResource, self).delete(**kwargs)

    @privilege_required(AuthenticatedPrivilege())
    def download_file(self, **kwargs):
        """
        ---
        get:
            description: Get the raw file for a file sample object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The raw file is returned.
                400:
                    description: There is no file available for this sample.
                404:
                    description: No sample with the specified id has been found.
        """
        try:
            sample = self.queryset().get(id=kwargs['id'])
            if not isinstance(sample, FileSample):
                return jsonify({'error': 'There is no file available for this sample'}), 400
            else:
                file = sample.file.read()
                return file, 200, {'Content-Type': 'application/octet-stream'}
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404

    @privilege_required(AuthenticatedPrivilege())
    def submit_file(self):
        """
        ---
        post:
            description: Upload a file sample to the MASS server
            parameters:
                - in: formData
                  name: file
                  type: file
            responses:
                201:
                    description: The file sample has been uploaded to the MASS server. The metadata of the sample is returned.
                    schema: FileSampleSchema
                400:
                    description: No file has been attached to the request or the request is malformed.
        """
        if 'file' not in request.files:
            return jsonify({'error': 'File payload missing in POST request.'}), 400
        else:
            if 'metadata' in request.form:
                metadata = json.loads(request.form['metadata'])
            else:
                metadata = {}
            data = {
                'file': request.files['file']
            }
            data.update(metadata)
            sample = FileSample.create_or_update(**data)
            sample.save()
            sample = Sample.objects.get(id=sample.id)
            schema = SchemaMapping.get_schema_for_model_class(sample.__class__.__name__)
            return jsonify(schema().dump(sample).data), 201

    @privilege_required(AuthenticatedPrivilege())
    def submit_ip(self):
        """
        ---
        post:
            description: Submit an IP address to the MASS server
            parameters:
                - in: body
                  name: body
                  type: string
            responses:
                201:
                    description: The IP address sample has been created on the MASS server. The metadata of the sample is returned.
                    schema: IPSampleSchema
                400:
                    description: No IP address has been given or the request is malformed.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        else:
            sample = IPSample.create_or_update(**json_data)
            sample.save()
            schema = SchemaMapping.get_schema_for_model_class(sample.__class__.__name__)
            return jsonify(schema().dump(sample).data), 201

    @privilege_required(AuthenticatedPrivilege())
    def submit_domain(self):
        """
        ---
        post:
            description: Submit a domain name to the MASS server
            parameters:
                - in: body
                  name: body
                  type: string
            responses:
                201:
                    description: The domain name sample has been created on the MASS server. The metadata of the sample is returned.
                    schema: DomainSampleSchema
                400:
                    description: No domain name has been given or the request is malformed.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        else:
            sample = DomainSample.create_or_update(**json_data)
            sample.save()
            schema = SchemaMapping.get_schema_for_model_class(sample.__class__.__name__)
            return jsonify(schema().dump(sample).data), 201

    @privilege_required(AuthenticatedPrivilege())
    def submit_uri(self):
        """
        ---
        post:
            description: Submit a URI to the MASS server
            parameters:
                - in: body
                  name: body
                  type: string
            responses:
                201:
                    description: The URI sample has been created on the MASS server. The metadata of the sample is returned.
                    schema: URISampleSchema
                400:
                    description: No URI has been given or the request is malformed.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        else:
            sample = URISample.create_or_update(**json_data)
            sample.save()
            schema = SchemaMapping.get_schema_for_model_class(sample.__class__.__name__)
            return jsonify(schema().dump(sample).data), 201

    @privilege_required(AuthenticatedPrivilege())
    def reports(self, **kwargs):
        """
        ---
        get:
            description: Get the reports associated to the given sample
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The list of reports is returned.
                    schema: ReportSchema
                404:
                    description: No sample with the specified id has been found.
        """
        try:
            sample = self.queryset().get(id=kwargs['id'])
            reports = Report.objects(sample=sample)
            serialized_result = ReportSchema(many=True).dump(reports)
            return jsonify({
                'results': serialized_result.data,
            })
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404

    @privilege_required(AuthenticatedPrivilege())
    def relation_graph(self, **kwargs):
        """
        ---
        get:
            description: Get a graph representation of the sample relations of the given sample
            parameters:
                - in: path
                  name: id
                  type: string
                - in: query
                  name: depth
                  type: integer
            responses:
                200:
                    description: The relation graph is returned.
                404:
                    description: No sample with the specified id has been found.
        """
        try:
            sample = self.queryset().get(id=kwargs['id'])
            if 'depth' in request.args:
                sample_relations = GraphFunctions.get_relation_graph(sample, int(request.args['depth']))
            else:
                sample_relations = GraphFunctions.get_relation_graph(sample)
            serialized_sample_relations = []
            for sample_relation in sample_relations:
                schema = SchemaMapping.get_schema_for_model_class(sample_relation.__class__.__name__)
                serialized_sample_relations.append(schema().dump(sample_relation).data)
            return jsonify({
                'results': serialized_sample_relations
            })
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404


register_api_endpoint('sample', SampleResource)

api_blueprint.add_url_rule('/sample/<id>/download/', view_func=SampleResource().download_file, methods=['GET'], endpoint='sample_download')
api_blueprint.apispec.add_path(path='/sample/{id}/download/', view=SampleResource.download_file)

api_blueprint.add_url_rule('/sample/submit_file/', view_func=SampleResource().submit_file, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample/submit_file/', view=SampleResource.submit_file)

api_blueprint.add_url_rule('/sample/submit_ip/', view_func=SampleResource().submit_ip, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample/submit_ip/', view=SampleResource.submit_ip)

api_blueprint.add_url_rule('/sample/submit_domain/', view_func=SampleResource().submit_domain, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample/submit_domain/', view=SampleResource.submit_domain)

api_blueprint.add_url_rule('/sample/submit_uri/', view_func=SampleResource().submit_uri, methods=['POST'])
api_blueprint.apispec.add_path(path='/sample/submit_uri/', view=SampleResource.submit_uri)

api_blueprint.add_url_rule('/sample/<id>/reports/', view_func=SampleResource().reports, methods=['GET'], endpoint='sample_reports')
api_blueprint.apispec.add_path(path='/sample/{id}/reports/', view=SampleResource.reports)

api_blueprint.add_url_rule('/sample/<id>/relation_graph/', view_func=SampleResource().relation_graph, methods=['GET'], endpoint='sample_relation_graph')
api_blueprint.apispec.add_path(path='/sample/{id}/relation_graph/', view=SampleResource.relation_graph)
