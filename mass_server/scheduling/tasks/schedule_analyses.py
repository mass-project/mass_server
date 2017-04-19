import sys

from flask import current_app

from mass_server.core.models import AnalysisSystemInstance, ScheduledAnalysis, AnalysisRequest


def _prepare_instance_dict():
    instance_dict = {}
    instances = AnalysisSystemInstance.objects().no_dereference()
    for instance in instances:
        if instance.analysis_system.id not in instance_dict.keys():
            instance_dict[instance.analysis_system.id] = list()
        if not instance.is_online:
            continue
        instance.analyses_count = ScheduledAnalysis.objects(analysis_system_instance=instance).count()
        if instance.analyses_count <= current_app.config['MAX_SCHEDULE_THRESHOLD']:
            instance_dict[instance.analysis_system.id].append(instance)
    return instance_dict


def _get_instance_with_minimum_count(instance_list):
    min_count = sys.maxsize
    min_instance = None
    for instance in instance_list:
        if instance.analyses_count < min_count:
            min_count = instance.analyses_count
            min_instance = instance
    return min_instance


def _schedule_analysis(request, instance):
    s = ScheduledAnalysis(analysis_system_instance=instance, sample=request.sample)
    s.save()
    instance.analyses_count += 1


def _schedule_analysis_request(request, instance_dict):
    if request.analysis_system.id not in instance_dict:
        return False

    instances = instance_dict[request.analysis_system.id]

    if len(instances) == 0:
        return False

    min_instance = _get_instance_with_minimum_count(instances)
    _schedule_analysis(request, min_instance)
    if min_instance.analyses_count > current_app.config['MAX_SCHEDULE_THRESHOLD']:
        instances.remove(min_instance)
    return True


def schedule_analyses():
    with current_app.app_context():
        instance_dict = _prepare_instance_dict()
        analysis_requests = AnalysisRequest.objects().no_dereference()
        requests_scheduled = 0
        requests_not_scheduled = 0
        for request in analysis_requests:
            if _schedule_analysis_request(request, instance_dict):
                request.delete()
                requests_scheduled += 1
            else:
                requests_not_scheduled += 1
