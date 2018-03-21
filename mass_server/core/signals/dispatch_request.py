from mass_server.core.models import Sample, AnalysisSystem, AnalysisRequest, ScheduledAnalysis
from mass_server.core.utils.tag_parser import TagParser
from datetime import datetime, timedelta


def _filter_matches_tags(tags, tag_filter):
    return TagParser(tags).parse_string(tag_filter)


def _match_sample_and_system(sample, system):
    if system in sample.dispatched_to:
        return
    if not _filter_matches_tags(sample.tags, system.tag_filter_expression):
        return

    for time_offset in system.time_schedule:
        schedule_after = datetime.now() + timedelta(minutes=time_offset)
        analysis_request = AnalysisRequest(sample=sample, analysis_system=system, schedule_after=schedule_after)
        analysis_request.save()

    sample.dispatched_to.append(system)
    sample.save()


def update_dispatch_request_for_sample(sender, document, **kwargs):
    for system in AnalysisSystem.objects():
        _match_sample_and_system(document, system)


def create_requests_for_new_analysis_system(sender, document, **kwargs):
    if not issubclass(sender, AnalysisSystem):
        return
    if kwargs.get('created') is True:
        for sample in Sample.objects():
            _match_sample_and_system(sample, document)


def create_requests_for_deleted_analysis_system_instance(sender, document, **kwargs):
    scheduled_analyses = ScheduledAnalysis.objects(analysis_system_instance=document)
    for analysis in scheduled_analyses:
        r = AnalysisRequest(analysis_system=document.analysis_system, sample=analysis.sample, parameters=analysis.parameters)
        r.save()
        analysis.delete()
