from .base import BaseResource
from flask import request
from flask import jsonify
from mass_flask_api.schemas import SampleRelationSchema
from mass_flask_core.models import SampleRelation
from mass_flask_api.utils import get_pagination_compatible_schema
from mass_flask_api.utils import register_api_endpoint
from mass_flask_core.models import Sample


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
                    description: A list of relations is returned.
                    schema: SampleRelationSchema
        """
        return super(SampleRelationResource, self).get_list()

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single relation object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The relation is returned.
                    schema: SampleRelationSchema
                404:
                    description: No relation with the specified id has been found.
        """
        return super(SampleRelationResource, self).get_detail(**kwargs)

    def post(self):
        """
        ---
        post:
            description: Create a new relation
            parameters:
                - in: body
                  name: body
                  schema: SampleRelationSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: SampleRelationSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        return super(SampleRelationResource, self).post()

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
                  schema: SampleRelationSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: SampleRelationSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No relation with the specified id has been found.
        """
        return super(SampleRelationResource, self).put(**kwargs)

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


register_api_endpoint('sample_relation', SampleRelationResource)
