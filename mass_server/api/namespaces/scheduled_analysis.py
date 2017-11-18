import json

from flask import request, jsonify
from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate, filter_results

from mass_server.api.config import api
from mass_server.api.schemas import ScheduledAnalysisSchema, ReportSchema
from mass_server.api.utils import pagination_helper, MappedQuerysetFilter
from mass_server.core.models import ScheduledAnalysis


@api.add_namespace('/scheduled_analysis')
class ScheduledAnalysisNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(ScheduledAnalysisSchema(), paginated=True)
    @paginate(pagination_helper)
    @filter_results(MappedQuerysetFilter(ScheduledAnalysis.filter_parameters), ScheduledAnalysis.filter_parameters.keys())
    def collection_get(self):
        return ScheduledAnalysis.objects

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/', methods=['POST'])
    @dump(ScheduledAnalysisSchema(), return_code=201)
    @load(ScheduledAnalysisSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(ScheduledAnalysis.DoesNotExist,
           'No scheduled analysis with the specified id found.', 404)
    @dump(ScheduledAnalysisSchema())
    def element_get(self, id):
        return ScheduledAnalysis.objects.get(id=id)

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/submit_report/', methods=['POST'])
    @catch(ScheduledAnalysis.DoesNotExist,
           'No scheduled analysis with the specified id found.', 404)
    @dump(ReportSchema(), return_code=201)
    def element_report(self, id):
        scheduled_analysis = ScheduledAnalysis.objects.get(id=id)
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
        return report

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(ScheduledAnalysis.DoesNotExist,
           'No scheduled analysis with the specified id found.', 404)
    def element_delete(self, id):
        obj = ScheduledAnalysis.objects.get(id=id)
        obj.delete()
        return '', 204
