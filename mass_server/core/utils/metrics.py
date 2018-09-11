import inspect

from prometheus_client.core import GaugeMetricFamily

from mass_server import db
from mass_server.core import models
from mass_server.core.models import AnalysisSystem, Report


def get_db_statistics():
    result = []
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and issubclass(obj, db.Document):
            result.append((name, obj.objects.count()))
    return result


class DatabaseCollector:
    def collect(self):
        for name, value in get_db_statistics():
            yield GaugeMetricFamily('mass_db_{}'.format(name), 'Number of "{}" instances.'.format(name), value=value)

        reports_fail = GaugeMetricFamily('mass_db_reports_failed', 'Reports with status "failure" for each system',
                                         labels=['analysis_system'])
        reports_unrecv = GaugeMetricFamily('mass_db_reports_unrecv',
                                           'Reports with status "unrecoverable failure" for each system',
                                           labels=['analysis_system'])
        reports_ok = GaugeMetricFamily('mass_db_reports_succ', 'Reports with status "success" for each system',
                                       labels=['analysis_system'])
        for system in AnalysisSystem.objects:
            name = system.identifier_name
            reports_fail.add_metric([name], Report.objects.filter(analysis_system=system,
                                                                  status=Report.REPORT_STATUS_CODE_FAILURE).count())
            reports_unrecv.add_metric([name], Report.objects.filter(analysis_system=system,
                                                                    status=Report.REPORT_STATUS_CODE_UNRECOVERABLE_FAIL).count())
            reports_ok.add_metric([name], Report.objects.filter(analysis_system=system,
                                                                status=Report.REPORT_STATUS_CODE_OK).count())

        yield reports_fail
        yield reports_unrecv
        yield reports_ok
