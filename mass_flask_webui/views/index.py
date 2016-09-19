import datetime

from flask import render_template

from mass_flask_core.models import Sample
from mass_flask_core.utils import TimeFunctions
from mass_flask_webui.config import webui_blueprint


def _get_sample_statistics():
    result = []
    now = TimeFunctions.get_timestamp().replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(0,14):
        start = now - datetime.timedelta(days=i)
        end = now - datetime.timedelta(days=i-1)
        number = Sample.objects(delivery_date__gte=start, delivery_date__lt=end).count()
        result.append((start, number))
    return result


@webui_blueprint.route('/')
def index():
    index_context = {
        'latest_samples': Sample.objects.get_with_tlp_level_filter().limit(10),
        'sample_statistics': _get_sample_statistics()
    }

    return render_template('index.html', **index_context)
