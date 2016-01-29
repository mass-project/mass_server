from .base import BaseResource
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_api.schemas import AnalysisRequestSchema
from mass_flask_core.models import AnalysisRequest


class AnalysisRequestResource(BaseResource):
    schema = AnalysisRequestSchema()
    pagination_schema = get_pagination_compatible_schema(AnalysisRequestSchema)
    model = AnalysisRequest
    query_key_field = 'id'

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all analysis requests.
            responses:
                200:
                    description: A list of analysis requests is returned.
                    schema: AnalysisRequestSchema
        """
        return super(AnalysisRequestResource, self).get_list()

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single analysis request object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The analysis request is returned.
                    schema: AnalysisRequestSchema
                404:
                    description: No analysis request with the specified id has been found.
        """
        return super(AnalysisRequestResource, self).get_detail(**kwargs)

    def post(self):
        """
        ---
        post:
            description: Create a new analysis request
            parameters:
                - in: body
                  name: body
                  schema: AnalysisRequestSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: AnalysisRequestSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        return super(AnalysisRequestResource, self).post()

    def put(self, **kwargs):
        """
        ---
        put:
            description: Update an existing analysis request object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: AnalysisRequestSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: AnalysisRequestSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No analysis request with the specified id has been found.
        """
        return super(AnalysisRequestResource, self).put(**kwargs)

    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing analysis request object
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
                    description: No analysis request with the specified id has been found.
        """
        return super(AnalysisRequestResource, self).delete(**kwargs)


register_api_endpoint('analysis_request', AnalysisRequestResource)
