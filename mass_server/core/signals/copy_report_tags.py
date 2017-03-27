from mass_server.core.models import Report


def copy_tags_from_report_to_sample(sender, document, **kwargs):
    if not issubclass(sender, Report):
        return
    document.sample.add_tags(document.tags)
