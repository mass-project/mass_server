from mongoengine import signals
from mass_flask_core.models import AnalysisSystem, Report
from .dispatch_request import update_dispatch_request_for_new_sample, create_requests_for_new_analysis_system
from .copy_report_tags import copy_tags_from_report_to_sample


def connect_signals():
    signals.post_save.connect(update_dispatch_request_for_new_sample)
    signals.post_save.connect(create_requests_for_new_analysis_system, sender=AnalysisSystem)
    signals.post_save.connect(copy_tags_from_report_to_sample, sender=Report)

