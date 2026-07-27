# utils/pagination.py

from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page=10, page_param='page'):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(page_param)

    return paginator.get_page(page_number)