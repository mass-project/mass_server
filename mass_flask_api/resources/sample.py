from flask import jsonify, request

from mass_flask_api.config import api_blueprint
from mass_flask_api.schemas import SampleSchema, FileSampleSchema, ExecutableBinarySampleSchema
from mass_flask_core.models import Sample, FileSample

from .base import BaseResource
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint


def _get_schema_for_model_class(model_class_name):
    model_conversion = {
        'Sample': SampleSchema,
        'FileSample': FileSampleSchema,
        'ExecutableBinarySample': ExecutableBinarySampleSchema
    }
    if model_class_name in model_conversion:
        return model_conversion[model_class_name]
    else:
        raise ValueError('Unsupported model type: {}'.format(model_class_name))


class SampleResource(BaseResource):
    schema = SampleSchema()
    pagination_schema = get_pagination_compatible_schema(SampleSchema)
    model = Sample
    query_key_field = 'id'

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all samples.
            responses:
                200:
                    description: A list of samples is returned.
                    schema: SampleSchema
        """
        serialized_samples = []
        paginated_samples = self._get_list()
        for sample in paginated_samples['results']:
            schema = _get_schema_for_model_class(sample.__class__.__name__)
            serialized_samples.append(schema().dump(sample).data)
        return jsonify({
            'results': serialized_samples,
            'next': paginated_samples['next'],
            'previous': paginated_samples['previous']
        })

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
        sample = self.model.objects(id=kwargs['id']).first()
        if not sample:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
        else:
            schema = _get_schema_for_model_class(sample.__class__.__name__)
            return jsonify(schema().dump(sample).data)

    def post(self):
        return jsonify({'error': 'Posting samples directly to the sample endpoint is not allowed. Instead please use the respective endpoints of each specific sample type.'}), 400

    def put(self, **kwargs):
        return jsonify({'error': 'Updating sample objects via the API is not supported yet.'}), 400

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
        sample = self.model.objects(id=kwargs['id']).first()
        if not sample:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
        elif not isinstance(sample, FileSample):
            return jsonify({'error': 'There is no file available for this sample'}), 400
        else:
            file = sample.file.read()
            return file, 200, {'Content-Type': 'application/octet-stream'}

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
            data = {
                'file': request.files['file']
            }
            sample = FileSample.create_or_update(**data)
            print(sample)
            sample.save()
            schema = _get_schema_for_model_class(sample.__class__.__name__)
            return jsonify(schema().dump(sample).data), 201


register_api_endpoint('sample', SampleResource)

api_blueprint.add_url_rule('/sample/<id>/download/', view_func=SampleResource().download_file, methods=['GET'], endpoint='sample_download')
api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + '/sample/{id}/download/', view=SampleResource.download_file)

api_blueprint.add_url_rule('/sample/submit_file/', view_func=SampleResource().submit_file, methods=['POST'])
api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + '/sample/submit_file/', view=SampleResource.submit_file)
