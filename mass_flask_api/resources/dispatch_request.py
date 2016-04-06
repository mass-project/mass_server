from flask import jsonify, request

from mass_flask_api.config import api_blueprint
from .base import BaseResource
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_api.schemas import DispatchRequestSchema, AnalysisRequestSchema
from mass_flask_core.models import DispatchRequest


class DispatchRequestResource(BaseResource):
    schema = DispatchRequestSchema()
    pagination_schema = get_pagination_compatible_schema(DispatchRequestSchema)
    model = DispatchRequest
    query_key_field = 'id'
    filter_parameters = []

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all dispatch requests.
            responses:
                200:
                    description: A list of dispatch requests is returned.
                    schema: DispatchRequestSchema
        """
        return super(DispatchRequestResource, self).get_list()

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single dispatch request object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The dispatch request is returned.
                    schema: DispatchRequestSchema
                404:
                    description: No dispatch request with the specified id has been found.
        """
        return super(DispatchRequestResource, self).get_detail(**kwargs)

    def post(self):
        """
        ---
        post:
            description: Create a new dispatch request
            parameters:
                - in: body
                  name: body
                  schema: DispatchRequestSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: DispatchRequestSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        return super(DispatchRequestResource, self).post()

    def put(self, **kwargs):
        """
        ---
        put:
            description: Update an existing dispatch request object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: DispatchRequestSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: DispatchRequestSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No dispatch request with the specified id has been found.
        """
        return super(DispatchRequestResource, self).put(**kwargs)

    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing dispatch request object
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
                    description: No dispatch request with the specified id has been found.
        """
        return super(DispatchRequestResource, self).delete(**kwargs)

    def dispatch_to_systems(self, **kwargs):
        """
        ---
        post:
            description: Dispatch the sample of a dispatch request to a number of analysis systems
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: AnalysisRequestSchema
            responses:
                204:
                    description: The sample has been dispatched for analysis on the specified analysis systems. The dispatch request object has been deleted.
                400:
                    description: The server was not able to process the request based on the request data.
                404:
                    description: No dispatch request with the specified id has been found.
        """
        dispatch_request = self.model.objects(id=kwargs['id']).first()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        elif not dispatch_request:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404
        else:
            parsed_data = AnalysisRequestSchema().load(json_data, partial=True, many=True)
            if parsed_data.errors:
                return jsonify(parsed_data.errors), 400
            for item in parsed_data.data:
                item.sample = dispatch_request.sample
                item.priority = dispatch_request.priority
                item.save()
            dispatch_request.delete()
            return '', 204


register_api_endpoint('dispatch_request', DispatchRequestResource)

api_blueprint.add_url_rule('/dispatch_request/<id>/dispatch_to_systems/', view_func=DispatchRequestResource().dispatch_to_systems, methods=['POST'])
api_blueprint.apispec.add_path('/dispatch_request/{id}/dispatch_to_systems/', view=DispatchRequestResource.dispatch_to_systems)
