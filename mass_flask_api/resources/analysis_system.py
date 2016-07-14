from mass_flask_api.schemas import AnalysisSystemSchema
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_core.models import AnalysisSystem
from mass_flask_core.utils import AuthFunctions, AdminAccessPrivilege
from .base import BaseResource


class AnalysisSystemResource(BaseResource):
    schema = AnalysisSystemSchema()
    pagination_schema = get_pagination_compatible_schema(AnalysisSystemSchema)
    model = AnalysisSystem
    query_key_field = 'identifier_name'
    filter_parameters = []

    @AuthFunctions.check_api_key()
    def get_list(self):
        """
        ---
        get:
            description: Get a list of all analysis systems.
            responses:
                200:
                    description: A list of analysis systems is returned.
                    schema: AnalysisSystemSchema
        """
        return super(AnalysisSystemResource, self).get_list()

    @AuthFunctions.check_api_key()
    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single analysis system object
            parameters:
                - in: path
                  name: identifier_name
                  type: string
            responses:
                200:
                    description: The analysis system is returned.
                    schema: AnalysisSystemSchema
                404:
                    description: No analysis system with the specified identifier_name has been found.
        """
        return super(AnalysisSystemResource, self).get_detail(**kwargs)

    @AuthFunctions.check_api_key(privileges=[AdminAccessPrivilege()])
    def post(self):
        """
        ---
        post:
            description: Create a new analysis system
            parameters:
                - in: body
                  name: body
                  schema: AnalysisSystemSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: AnalysisSystemSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        return super(AnalysisSystemResource, self).post()

    @AuthFunctions.check_api_key(privileges=[AdminAccessPrivilege()])
    def put(self, **kwargs):
        """
        ---
        put:
            description: Update an existing analysis system object
            parameters:
                - in: path
                  name: identifier_name
                  type: string
                - in: body
                  name: body
                  schema: AnalysisSystemSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: AnalysisSystemSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No analysis system with the specified identifier_name has been found.
        """
        return super(AnalysisSystemResource, self).put(**kwargs)

    @AuthFunctions.check_api_key(privileges=[AdminAccessPrivilege()])
    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing analysis system object
            parameters:
                - in: path
                  name: identifier_name
                  type: string
            responses:
                204:
                    description: The object has been deleted.
                400:
                    description: The server was not able to delete an object based on the request data.
                404:
                    description: No analysis system with the specified identifier_name has been found.
        """
        return super(AnalysisSystemResource, self).delete(**kwargs)


register_api_endpoint('analysis_system', AnalysisSystemResource)
