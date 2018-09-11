import inspect

from prometheus_client.core import GaugeMetricFamily

from mass_server import db
from mass_server.core import models


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
