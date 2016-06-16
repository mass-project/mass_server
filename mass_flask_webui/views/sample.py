from flask import render_template

from mass_flask_core.models import Sample, Report
from mass_flask_core.utils import PaginationFunctions
from mass_flask_webui.config import webui_blueprint


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
