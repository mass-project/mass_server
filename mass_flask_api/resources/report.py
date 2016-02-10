from .base import BaseResource
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_api.schemas import ReportSchema
from mass_flask_core.models import Report


class ReportResource(BaseResource):
    schema = ReportSchema()
    pagination_schema = get_pagination_compatible_schema(ReportSchema)
    model = Report
    query_key_field = 'id'
    filter_parameters = []

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all reports.
            responses:
                200:
                    description: A list of reports is returned.
                    schema: ReportSchema
        """
        return super(ReportResource, self).get_list()

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single report object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The report is returned.
                    schema: ReportSchema
                404:
                    description: No report with the specified id has been found.
        """
        return super(ReportResource, self).get_detail(**kwargs)

    def post(self):
        """
        ---
        post:
            description: Create a new report
            parameters:
                - in: body
                  name: body
                  schema: ReportSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: ReportSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        return super(ReportResource, self).post()

    def put(self, **kwargs):
        """
        ---
        put:
            description: Update an existing report object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: ReportSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: ReportSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No report with the specified id has been found.
        """
        return super(ReportResource, self).put(**kwargs)

    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing report object
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
                    description: No report with the specified id has been found.
        """
        return super(ReportResource, self).delete(**kwargs)


register_api_endpoint('report', ReportResource)
