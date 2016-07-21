from mass_flask_core.models import Sample, AnalysisSystem, AnalysisRequest
from mass_flask_core.utils.tag_parser import TagParser


def _filter_matches_tags(tags, tag_filter):
    return TagParser(tags).parse_string(tag_filter)


def _find_matching_systems_for_sample(sample):
    for item in AnalysisSystem.objects():
        if item in sample.dispatched_to:
            continue
        if not _filter_matches_tags(sample.tags, item.tag_filter_expression):
            continue
        analysis_request = AnalysisRequest(sample=sample, analysis_system=item)
        analysis_request.save()
        sample.dispatched_to.append(item)
    sample.save()


def update_dispatch_request_for_new_sample(sender, document, **kwargs):
    if not issubclass(sender, Sample):
        return
    if kwargs.get('created') is True:
        _find_matching_systems_for_sample(document)
