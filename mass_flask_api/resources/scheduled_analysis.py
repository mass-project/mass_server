from flask import request, jsonify

from mass_flask_api.config import api_blueprint
from .base import BaseResource
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_api.schemas import ScheduledAnalysisSchema, ReportSchema
from mass_flask_core.models import ScheduledAnalysis


class ScheduledAnalysisResource(BaseResource):
    schema = ScheduledAnalysisSchema()
    pagination_schema = get_pagination_compatible_schema(ScheduledAnalysisSchema)
    model = ScheduledAnalysis
    query_key_field = 'id'
    filter_parameters = []

    def get_list(self):
        """
        ---
        get:
            description: Get a list of all scheduled analyses.
            responses:
                200:
                    description: A list of scheduled analyses is returned.
                    schema: ScheduledAnalysisSchema
        """
        return super(ScheduledAnalysisResource, self).get_list()

    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single scheduled analysis object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The scheduled analysis is returned.
                    schema: ScheduledAnalysisSchema
                404:
                    description: No scheduled analysis with the specified id has been found.
        """
        return super(ScheduledAnalysisResource, self).get_detail(**kwargs)

    def post(self):
        """
        ---
        post:
            description: Create a new scheduled analysis
            parameters:
                - in: body
                  name: body
                  schema: ScheduledAnalysisSchema
            responses:
                201:
                    description: The object has been created. The reply contains the newly created object.
                    schema: ScheduledAnalysisSchema
                400:
                    description: The server was not able to create an object based on the request data.
        """
        return super(ScheduledAnalysisResource, self).post()

    def put(self, **kwargs):
        """
        ---
        put:
            description: Update an existing scheduled analysis object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: ScheduledAnalysisSchema
            responses:
                200:
                    description: The object has been updated. The reply contains the updated object.
                    schema: ScheduledAnalysisSchema
                400:
                    description: The server was not able to update an object based on the request data.
                404:
                    description: No scheduled analysis with the specified id has been found.
        """
        return super(ScheduledAnalysisResource, self).put(**kwargs)

    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing scheduled analysis object
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
                    description: No scheduled analysis with the specified id has been found.
        """
        return super(ScheduledAnalysisResource, self).delete(**kwargs)

    def submit_report(self, **kwargs):
        """
        ---
        post:
            description: Submit the report for the specified scheduled analysis
            parameters:
                - in: path
                  name: id
                  type: string
                - in: body
                  name: body
                  schema: ReportSchema
            responses:
                204:
                    description: The report has been submitted. The scheduled analysis object has been deleted.
                400:
                    description: The server was not able to process the request based on the request data.
                404:
                    description: No scheduled analysis with the specified id has been found.
        """
        scheduled_analysis = self.model.objects(id=kwargs['id']).first()
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        elif not scheduled_analysis:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404
        else:
            parsed_report = ReportSchema().load(json_data, partial=True)
            if parsed_report.errors:
                return jsonify(parsed_report.errors), 400
            report = parsed_report.data
            report.sample = scheduled_analysis.sample
            report.analysis_system = scheduled_analysis.analysis_system_instance.analysis_system
            report.save()
            scheduled_analysis.delete()
            return '', 204


register_api_endpoint('scheduled_analysis', ScheduledAnalysisResource)

api_blueprint.add_url_rule('/scheduled_analysis/<id>/submit_report/', view_func=ScheduledAnalysisResource().submit_report, methods=['POST'])
api_blueprint.apispec.add_path(path=api_blueprint.config['API_PREFIX'] + '/scheduled_analysis/{id}/submit_report/', view=ScheduledAnalysisResource.submit_report)
