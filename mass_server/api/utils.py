from flask import url_for, request
from math import ceil
from flask_slimrest.pagination import PaginationResult
from flask_slimrest.utils import make_api_response


def _get_page_link(page_number):
    return url_for(request.url_rule.endpoint, page=page_number, _external=True, **request.view_args)


def pagination_helper(queryset, per_page=100):
    item_count = queryset.count()

    if 'count' in request.args:
        return make_api_response({'count': item_count})

    if 'page' in request.args:
        page = int(request.args['page'])
    else:
        page = 1

    page_count = ceil(item_count/per_page)
    paginated_queryset = queryset.paginate(page=page, per_page=per_page)

    return PaginationResult(
        paginated_queryset.items,
        page,
        page_count,
        _get_page_link(paginated_queryset.next_num) if paginated_queryset.has_next else None,
        _get_page_link(paginated_queryset.prev_num) if paginated_queryset.has_prev else None
    )


def filter_queryset(queryset, **kwargs):
    return queryset.filter(**kwargs)


class MappedQuerysetFilter:
    def __init__(self, mapping):
        self.mapping = mapping

    def __call__(self, queryset, **kwargs):
        passed_args = {}
        for arg, value in kwargs.items():
            if arg not in self.mapping:
                raise ValueError('Passed argument "{}" is not in the parameter mapping.'.format(arg))

            if self.mapping[arg]:
                passed_args[self.mapping[arg]] = value
            else:
                passed_args[arg] = value

        return filter_queryset(queryset, **passed_args)

