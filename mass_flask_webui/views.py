from flask import render_template, redirect, url_for

from mass_flask_core.models import Sample, Report, FileSample, ExecutableBinarySample, IPSample, DomainSample, URISample
from mass_flask_core.utils import PaginationFunctions
from mass_flask_webui.config import webui_blueprint
from mass_flask_webui.forms import FileSampleSubmitForm, IPSampleSubmitForm, DomainSampleSubmitForm, URISampleSubmitForm


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


@webui_blueprint.route('/apidocs/')
def apidocs():
    return render_template('apidocs.html')


@PaginationFunctions.paginate(per_page=100)
def _get_samples_paginated():
    return Sample.objects()


@webui_blueprint.route('/sample/')
def sample_list():
    samples = _get_samples_paginated()
    return render_template('sample_list.html', samples=samples)


@webui_blueprint.route('/sample/<sample_id>/')
def sample_detail(sample_id):
    sample = Sample.objects(id=sample_id).first()
    reports = Report.objects(sample=sample)
    return render_template('sample_detail.html', sample=sample, reports=reports)


@webui_blueprint.route('/submit/file/', methods=['GET', 'POST'])
def submit_file():
    form = FileSampleSubmitForm()
    if form.validate_on_submit():
        sample = FileSample.create_or_update(file=form.data['file'], **form.data['optional'])
        return redirect(url_for('mass_flask_webui.sample_detail', sample_id=sample.id))
    return render_template('submit.html', form=form)


@webui_blueprint.route('/submit/ip/', methods=['GET', 'POST'])
def submit_ip():
    form = IPSampleSubmitForm()
    if form.validate_on_submit():
        sample = IPSample.create_or_update(ip_address=form.data['ip_address'], **form.data['optional'])
        return redirect(url_for('mass_flask_webui.sample_detail', sample_id=sample.id))
    return render_template('submit.html', form=form)


@webui_blueprint.route('/submit/domain/', methods=['GET', 'POST'])
def submit_domain():
    form = DomainSampleSubmitForm()
    if form.validate_on_submit():
        sample = DomainSample.create_or_update(domain=form.data['domain'], **form.data['optional'])
        return redirect(url_for('mass_flask_webui.sample_detail', sample_id=sample.id))
    return render_template('submit.html', form=form)


@webui_blueprint.route('/submit/uri/', methods=['GET', 'POST'])
def submit_uri():
    form = URISampleSubmitForm()
    if form.validate_on_submit():
        sample = URISample.create_or_update(uri=form.data['uri'], **form.data['optional'])
        return redirect(url_for('mass_flask_webui.sample_detail', sample_id=sample.id))
    return render_template('submit.html', form=form)
