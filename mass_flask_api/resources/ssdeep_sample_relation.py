from .base import BaseResource
from flask import request
from flask import jsonify
from mass_flask_api.schemas import SsdeepSampleRelationSchema
from mass_flask_core.models import SsdeepSampleRelation
from mass_flask_api.utils import get_pagination_compatible_schema
from mass_flask_api.utils import register_api_endpoint
from mass_flask_core.models import Sample


class SsdeepSampleRelationResource(BaseResource):
    schema = SsdeepSampleRelationSchema()
    pagination_schema = get_pagination_compatible_schema(SsdeepSampleRelationSchema)
    model = SsdeepSampleRelation
    query_key_field = 'id'
    filter_parameters = []

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all ssdeep sample relations.
            responses:
                200:
                    description: A list of ssdeep relations is returned.
                    schema: SsdeepSampleRelationSchema
        """
        return super(SsdeepSampleRelationResource, self).get_list()

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single ssdeep relation object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The ssdeep relation is returned.
                    schema: SsdeepSampleRelationSchema
                404:
                    description: No ssdeep relation with the specified id has been found.
        """
        return super(SsdeepSampleRelationResource, self).get_detail(**kwargs)

    def post(self):
        """
        ---
        post:
            description: Create a new ssdeep relation
            parameters:
                - in: body
                  name: body
                  schema: SsdeepSampleRelationSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: SsdeepSampleRelationSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        else:
            parsed_data = self.schema.load(json_data, partial=True)
            if parsed_data.errors:
                return jsonify(parsed_data.errors), 400
            obj = SsdeepSampleRelation()
            obj.sample = Sample.objects(id=json_data['sample']).first()
            obj.other = Sample.objects(id=json_data['other']).first()
            obj.match = json_data['match']
            obj.save()
            result = self.schema.dump(obj)
            return jsonify(result.data), 201

    def put(self, **kwargs):
        """
        ---
        put:
            description: Update an existing relation object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: SsdeepSampleRelationSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: SsdeepSampleRelationSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No relation with the specified id has been found.
        """
        return super(SsdeepSampleRelationResource, self).put(**kwargs)

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
        return super(SsdeepSampleRelationResource, self).delete(**kwargs)


register_api_endpoint('ssdeep_sample_relation', SsdeepSampleRelationResource)
