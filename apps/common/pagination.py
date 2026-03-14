from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    page_size: int = 20
    page_size_query_param: str = "page_size"
    max_page_size: int = 50