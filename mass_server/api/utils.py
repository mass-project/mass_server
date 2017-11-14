from flask import url_for, request
from math import ceil
from flask_slimrest.pagination import PaginationResult
from flask_slimrest.utils import make_api_response
from functools import wraps


def _get_page_link(page_number):
    return url_for(request.url_rule.endpoint, page=page_number, _external=True)


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


def apply_mapped_filters(filter_args={}):
    def real_decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            passed_args = {}
            for arg in request.args:
                if arg in filter_args:
                    if filter_args[arg]:
                        arg_name = filter_args[arg]
                    else:
                        arg_name = arg
                    passed_args[arg_name] = request.args[arg]
            return filter_queryset(function(self, *args, **kwargs), **passed_args)
        return wrapper
    return real_decorator
