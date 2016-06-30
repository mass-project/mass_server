from functools import wraps
from math import ceil

from flask import url_for, request


def _get_page_link(page_number):
    return url_for(request.url_rule.endpoint, page=page_number, _external=True)


class PaginationFunctions:
    @staticmethod
    def paginate(per_page=100):
        def real_decorator(view_function):
            @wraps(view_function)
            def paginate_function(*args, **kwargs):
                if 'page' in request.args:
                    page = int(request.args['page'])
                else:
                    page = 1
                queryset = view_function(*args, **kwargs)
                page_count = ceil(queryset.count()/per_page)
                paginated_queryset = queryset.paginate(page=page, per_page=per_page)
                result = {
                    'results': paginated_queryset.items,
                    'next': _get_page_link(paginated_queryset.next_num) if paginated_queryset.has_next else None,
                    'previous': _get_page_link(paginated_queryset.prev_num) if paginated_queryset.has_prev else None,
                    'page': page,
                    'page_count': page_count
                }
                return result
            return paginate_function
        return real_decorator
