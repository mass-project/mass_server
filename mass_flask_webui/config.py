from flask import Blueprint, render_template
from markupsafe import Markup

from mass_flask_config.app import app
from mass_flask_core.models import Sample, FileSample, IPSample, DomainSample, URISample, ExecutableBinarySample, Report
from mass_flask_core.utils.pagination_functions import paginate

webui_blueprint = Blueprint('mass_flask_webui', __name__, template_folder='templates', static_folder='static')

webui_blueprint.config = {
}


@webui_blueprint.route('/')
def index():
    index_context = {
        'latest_samples': Sample.objects().limit(10),
        'latest_reports': Report.objects().limit(10),
        'count_sample': Sample.objects().count(),
        'count_file_sample': FileSample.objects.count(),
        'count_executable_binary_sample': ExecutableBinarySample.objects().count(),
        'count_ip_sample': IPSample.objects().count(),
        'count_domain_sample': DomainSample.objects().count(),
        'count_uri_sample': URISample.objects().count()
    }

    return render_template('index.html', **index_context)


@paginate(per_page=100)
def get_samples_paginated():
    return Sample.objects()


@webui_blueprint.route('/sample/')
def sample_list():
    samples = get_samples_paginated()
    return render_template('sample_list.html', samples=samples)


@webui_blueprint.route('/sample/<sample_id>/')
def sample_detail(sample_id):
    sample = Sample.objects(id=sample_id).first()
    reports = Report.objects(sample=sample)
    return render_template('sample_detail.html', sample=sample, reports=reports)


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
        return app.version

    def pagination(paginator):
        return Markup(render_template('pagination.html', paginator=paginator))

    return dict(
        mass_version=mass_version,
        pagination=pagination
    )
