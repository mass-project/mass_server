from mass_flask_core.models import Sample, AnalysisSystem, AnalysisRequest
from mass_flask_core.utils.tag_parser import TagParser


def _filter_matches_tags(tags, tag_filter):
    return TagParser(tags).parse_string(tag_filter)


def _match_sample_and_system(sample, system):
    if system in sample.dispatched_to:
        return
    if not _filter_matches_tags(sample.tags, system.tag_filter_expression):
        return
    analysis_request = AnalysisRequest(sample=sample, analysis_system=system)
    analysis_request.save()
    sample.dispatched_to.append(system)
    sample.save()


def _find_matching_systems_for_sample(sample):
    for system in AnalysisSystem.objects():
        _match_sample_and_system(sample, system)


def _find_matching_samples_for_system(system):
    for sample in Sample.objects():
        _match_sample_and_system(sample, system)


def update_dispatch_request_for_new_sample(sender, document, **kwargs):
    if not issubclass(sender, Sample):
        return
    if kwargs.get('created') is True:
        _find_matching_systems_for_sample(document)


def create_requests_for_new_analysis_system(sender, document, **kwargs):
    if not issubclass(sender, AnalysisSystem):
        return
    if kwargs.get('created') is True:
        _find_matching_samples_for_system(document)