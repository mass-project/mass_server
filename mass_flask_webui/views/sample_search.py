from flask import render_template, request

from mass_flask_core.models import Sample
from mass_flask_core.utils import PaginationFunctions
from mass_flask_webui.config import webui_blueprint
from mass_flask_webui.forms.sample_search import SampleSearchForm


def _is_present_and_not_empty(form_data, variable):
    return variable in form_data and form_data[variable]


def _exact_fields_to_dict(form_data, exact_fields):
    result_dict = {}
    for field in exact_fields:
        if _is_present_and_not_empty(form_data, field):
            result_dict[field] = form_data[field]
    return result_dict


def _get_file_filters(file_form_data):
    exact_fields = [
        'mime_type',
        'file_names',
        'md5sum',
        'sha1sum',
        'sha256sum',
        'sha512sum',
        'file_size__lte',
        'file_size__gte',
        'shannon_entropy__lte',
        'shannon_entropy__gte'
    ]
    return _exact_fields_to_dict(file_form_data, exact_fields)


def _get_ip_filters(ip_form_data):
    exact_fields = [
        'ip_address'
    ]
    return _exact_fields_to_dict(ip_form_data, exact_fields)


def _get_domain_filters(domain_form_data):
    exact_fields = [
        'domain',
        'domain__contains',
        'domain__startswith',
        'domain__endswith'
    ]
    return _exact_fields_to_dict(domain_form_data, exact_fields)


def _get_uri_filters(uri_form_data):
    exact_fields = [
        'uri',
        'uri__contains',
        'uri__startswith',
        'uri__endswith'
    ]
    return _exact_fields_to_dict(uri_form_data, exact_fields)


def _get_common_filters(common_form_data):
    exact_fields = [
        'delivery_date__lte',
        'delivery_date__gte',
        'first_seen_date__lte',
        'first_seen_date__gte',
    ]
    result_dict = _exact_fields_to_dict(common_form_data, exact_fields)

    if _is_present_and_not_empty(common_form_data, 'tags'):
        tags = []
        for line in common_form_data['tags'].split('\r\n'):
            tags.append(line)
        result_dict['tags__all'] = tags

    return result_dict


@PaginationFunctions.paginate
def _build_query_from_form_data(form_data):
    queryset = Sample
    query_arguments = {}

    query_arguments.update(_get_common_filters(form_data['common']))
    query_arguments.update(_get_file_filters(form_data['file']))
    query_arguments.update(_get_ip_filters(form_data['ip']))
    query_arguments.update(_get_domain_filters(form_data['domain']))
    query_arguments.update(_get_uri_filters(form_data['uri']))

    query_result = queryset.objects(**query_arguments)
    return query_result


@webui_blueprint.route('/search/sample/', methods=['GET'])
def sample_search():
    form = SampleSearchForm(formdata=request.args)
    samples = []
    if 'submit' in request.args and form.validate():
        samples = _build_query_from_form_data(form.data)
    return render_template('sample_search.html', form=form, samples=samples)
