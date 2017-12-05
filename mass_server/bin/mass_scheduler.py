import sys
import time
import warnings
from multiprocessing import Pool

from mass_server import get_app
from mass_server.core.models import ScheduledAnalysis, AnalysisRequest, AnalysisSystemInstance


app = get_app()


class InstanceDict:
    _dict = {}

    @staticmethod
    def instance_dict():
        return InstanceDict._dict

    @staticmethod
    def update_instance_dict():
        InstanceDict._dict = {}
        instances = AnalysisSystemInstance.objects().no_dereference()
        for instance in instances:
            if instance.analysis_system.id not in InstanceDict._dict.keys():
                InstanceDict._dict[instance.analysis_system.id] = list()
            if not instance.is_online:
                continue
            instance.analyses_count = ScheduledAnalysis.objects(analysis_system_instance=instance).count()
            if instance.analyses_count <= app.config['MAX_SCHEDULE_THRESHOLD']:
                InstanceDict._dict[instance.analysis_system.id].append(instance)

    @staticmethod
    def get_instance_with_minimum_count(instance_list):
        min_count = sys.maxsize
        min_instance = None
        for instance in instance_list:
            if instance.analyses_count < min_count:
                min_count = instance.analyses_count
                min_instance = instance
        return min_instance

    @staticmethod
    def check_id(ident):
        if ident not in InstanceDict._dict:
            return False
        if len(InstanceDict._dict[ident]) == 0:
            return False
        return True

    @staticmethod
    def remove_if_threshold_reached(instance, system_id):
        if instance.analyses_count > app.config['MAX_SCHEDULE_THRESHOLD']:
            InstanceDict._dict[system_id].remove(instance)


def _schedule_analysis_request(request):
    system_id = request.analysis_system.id
    instances = InstanceDict._dict[system_id]
    min_instance = InstanceDict.get_instance_with_minimum_count(instances)
    if not InstanceDict.check_id(system_id):
        return False
    s = ScheduledAnalysis(analysis_system_instance=min_instance, sample=request.sample, parameters=request.parameters)
    s.save()
    min_instance.analyses_count += 1
    InstanceDict.remove_if_threshold_reached(min_instance, system_id)
    request.delete()
    return True


def schedule_analyses():
    print("Scheduling...")
    with app.app_context():
        InstanceDict.update_instance_dict()
        analysis_requests = AnalysisRequest.objects().no_dereference()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with Pool() as p:
                scheduled_list = p.map(_schedule_analysis_request, analysis_requests)
        requests_scheduled = sum(scheduled_list)
        request_not_scheduled = len(scheduled_list) - requests_scheduled
        print('Scheduled: ', requests_scheduled, 'Not scheduled: ', request_not_scheduled)


def main():
    while 1:
        schedule_analyses()
        time.sleep(app.config['SCHEDULE_ANALYSES_INTERVAL'])


if __name__ == '__main__':
    main()
