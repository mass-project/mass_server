from flask import request, jsonify, json
from flask_modular_auth import privilege_required, RolePrivilege
from mongoengine import DoesNotExist

from mass_server.core.models import ScheduledAnalysis
from mass_server.api.config import api_blueprint
from mass_server.api.schemas import ScheduledAnalysisSchema, ReportSchema
from mass_server.api.utils import get_pagination_compatible_schema, register_api_endpoint
from .base import BaseResource

import logging


class ScheduledAnalysisResource(BaseResource):
    schema = ScheduledAnalysisSchema()
    pagination_schema = get_pagination_compatible_schema(ScheduledAnalysisSchema)
    query_key_field = 'id'
    filter_parameters = []

    @privilege_required(RolePrivilege('admin'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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

    @privilege_required(RolePrivilege('admin'))
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
        return jsonify({'error': 'Method not allowed for this endpoint.'}), 405

    @privilege_required(RolePrivilege('admin'))
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

    @privilege_required(RolePrivilege('admin'), RolePrivilege('analysis_system_instance'))
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
        try:
            scheduled_analysis = self.schema.Meta.model.objects.get(id=kwargs['id'])

            if 'metadata' not in request.form:
                return jsonify({'error': 'JSON metadata missing in POST request.'}), 400
            else:
                data = json.loads(request.form['metadata'])
                data['json_report_objects'] = {}
                data['raw_report_objects'] = {}

                parsed_report = ReportSchema().load(data, partial=True)
                if parsed_report.errors:
                    return jsonify(parsed_report.errors), 400
                report = parsed_report.data

                report.sample = scheduled_analysis.sample
                report.analysis_system = scheduled_analysis.analysis_system_instance.analysis_system

                for key, f in request.files.items():
                    if f.mimetype == "application/json":
                        report.add_json_report_object(f)
                    else:
                        report.add_raw_report_object(f)

                report.save()
                scheduled_analysis.delete()
                return jsonify(ReportSchema().dump(report).data), 201
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404


register_api_endpoint('scheduled_analysis', ScheduledAnalysisResource)

api_blueprint.add_url_rule('/scheduled_analysis/<id>/submit_report/', view_func=ScheduledAnalysisResource().submit_report, methods=['POST'])
api_blueprint.apispec.add_path(path='/scheduled_analysis/{id}/submit_report/', view=ScheduledAnalysisResource.submit_report)
