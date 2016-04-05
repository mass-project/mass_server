from flask import current_app, render_template
from markupsafe import Markup

from mass_flask_core.models import FileSample, IPSample, DomainSample, URISample, ExecutableBinarySample
from mass_flask_webui.config import webui_blueprint


@webui_blueprint.context_processor
def sample_processors():
    def sample_icon(sample):
        if isinstance(sample, FileSample):
            return Markup('<i class="fa fa-file"></i>')
        elif isinstance(sample, IPSample):
            return Markup('<i class="fa fa-desktop"></i>')
        elif isinstance(sample, DomainSample):
            return Markup('<i class="fa fa-globe"></i>')
        elif isinstance(sample, URISample):
            return Markup('<i class="fa fa-at"></i>')
        else:
            return Markup('<i class="fa fa-question"></i>')

    def is_file_sample(sample):
        return isinstance(sample, FileSample)

    def is_executable_binary_sample(sample):
        return isinstance(sample, ExecutableBinarySample)

    return dict(
        sample_icon=sample_icon,
        is_file_sample=is_file_sample,
        is_executable_binary_sample=is_executable_binary_sample
    )


@webui_blueprint.context_processor
def generic_processors():
    def mass_version():
        return current_app.version

    def pagination(paginator):
        return Markup(render_template('pagination.html', paginator=paginator))

    return dict(
        mass_version=mass_version,
        pagination=pagination
    )
