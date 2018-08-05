import json

from flask import request, jsonify
from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, load_json, catch, paginate, filter_results
from flask_slimrest.utils import make_api_error_response

from mass_server.api.config import api
from mass_server.api.schemas import AnalysisRequestSchema, ReportSchema
from mass_server.api.utils import pagination_helper, MappedQuerysetFilter
from mass_server.core.models import AnalysisRequest, Report


@api.add_namespace('/analysis_request')
class AnalysisRequestNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(AnalysisRequestSchema(), paginated=True)
    @paginate(pagination_helper)
    @filter_results(MappedQuerysetFilter(AnalysisRequest.filter_parameters), AnalysisRequest.filter_parameters.keys())
    def collection_get(self):
        return AnalysisRequest.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(AnalysisRequestSchema(), return_code=201)
    @load(AnalysisRequestSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(AnalysisRequest.DoesNotExist,
           'No analysis request with the specified id found.', 404)
    @dump(AnalysisRequestSchema())
    def element_get(self, id):
        return AnalysisRequest.objects.get(id=id)

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/submit_report/', methods=['POST'])
    @catch(AnalysisRequest.DoesNotExist,
           'No scheduled analysis with the specified id found.', 404)
    @dump(ReportSchema(), return_code=201)
    def element_report(self, id):
        data = json.loads(request.form['metadata'])
        data['json_report_objects'] = {}
        data['raw_report_objects'] = {}

        parsed_report = ReportSchema().load(data, partial=True)
        if parsed_report.errors:
            return jsonify(parsed_report.errors), 400
        report = parsed_report.data
        report.post_deserialization(data=data, analysis_request_id=id)

        for key, f in request.files.items():
            if f.mimetype == "application/json":
                report.add_json_report_object(f)
            else:
                report.add_raw_report_object(f)

        report.save()
        return report

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['PATCH'])
    @catch(AnalysisRequest.DoesNotExist,
           'No analysis requested with the specified id found.', 404)
    @dump(AnalysisRequestSchema())
    @load_json
    def element_patch(self, id, data):
        obj = AnalysisRequest.objects.get(id=id)
        result = AnalysisRequestSchema().update(obj, data)
        if result.errors:
            return make_api_error_response(
                'Validation of the patched data has failed.', 400, {
                    'errors': result.errors
                })
        else:
            obj.save()
            return obj

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(AnalysisRequest.DoesNotExist,
           'No analysis request with the specified id found.', 404)
    def element_delete(self, id):
        obj = AnalysisRequest.objects.get(id=id)
        obj.delete()
        return '', 204
