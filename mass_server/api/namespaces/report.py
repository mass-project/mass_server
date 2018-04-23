from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, catch, paginate, filter_results

from mass_server.api.config import api
from mass_server.api.schemas import ReportSchema
from mass_server.api.utils import pagination_helper, MappedQuerysetFilter
from mass_server.core.models import Report


@api.add_namespace('/report')
class ReportNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(ReportSchema(), paginated=True)
    @paginate(pagination_helper)
    @filter_results(MappedQuerysetFilter(Report.filter_parameters), Report.filter_parameters.keys())
    def collection_get(self):
        return Report.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(ReportSchema(), return_code=201)
    @load(ReportSchema())
    def collection_post(self, data):
        obj = data.data
        obj.save()
        return obj

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(Report.DoesNotExist, 'No report with the specified id found.', 404)
    @dump(ReportSchema())
    def element_get(self, id):
        return Report.objects.get(id=id)

    @privilege_required(RolePrivilege('admin'))
    @add_endpoint('/<id>/', methods=['DELETE'])
    @catch(Report.DoesNotExist, 'No report with the specified id found.', 404)
    def element_delete(self, id):
        obj = Report.objects.get(id=id)
        obj.delete()
        return '', 204

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/json_report_object/<object_name>/')
    @catch(Report.DoesNotExist, 'No report with the specified id found.', 404)
    @catch(ValueError, 'No report object with the specified name found.', 404)
    def json_report_object(self, id, object_name):
        report = Report.objects.get(id=id)
        if object_name not in report.json_report_objects:
            raise ValueError('Report object not found.')
        return report.json_report_objects[object_name].read(), 200,  {'Content-Type': 'application/json'}

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/raw_report_object/<object_name>/')
    @catch(Report.DoesNotExist, 'No report with the specified id found.', 404)
    @catch(ValueError, 'No report object with the specified name found.', 404)
    def raw_report_object(self, id, object_name):
        report = Report.objects.get(id=id)
        if object_name not in report.raw_report_objects:
            raise ValueError('Report object not found.')
        return report.raw_report_objects[object_name].read(), 200,  {'Content-Type': 'application/octet-stream'}
