from mongoengine import signals
from mass_server.core.models import AnalysisSystem, Report, Sample
from .copy_report_tags import copy_tags_from_report_to_sample
from .dispatch_request import update_dispatch_request_for_sample, create_requests_for_new_analysis_system


def connect_signals():
    signals.post_save.connect(update_dispatch_request_for_sample, sender=Sample)
    signals.post_save.connect(create_requests_for_new_analysis_system, sender=AnalysisSystem)
    signals.post_save.connect(copy_tags_from_report_to_sample, sender=Report)
