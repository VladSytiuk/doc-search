from django.db.models import QuerySet


def paginate_queryset(
    queryset: QuerySet, first: int, limit: int, order_by: list
) -> QuerySet:
    if order_by:
        queryset = queryset.order_by(*order_by)
    if first:
        queryset = queryset[first:]
    if limit:
        queryset = queryset[:limit]
    return queryset
