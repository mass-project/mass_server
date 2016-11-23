from flask import render_template

from mass_flask_core.models import Sample, Report, FileSample, ExecutableBinarySample, IPSample, DomainSample, URISample
from mass_flask_webui.config import webui_blueprint


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
