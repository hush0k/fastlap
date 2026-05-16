import uuid
from contextvars import ContextVar
from logging import getLogger, Logger
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger: Logger = getLogger(__name__)

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id: str = str(uuid.uuid4())
        request_id_var.set(request_id)

        response: HttpResponse = self.get_response(request)
        response["X-Request-ID"] = request_id

        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        logger.debug(
            '"%s %s" | %s | %s |',
            request.method,
            request.path,
            request.META.get("REMOTE_ADDR"),
            request.META.get("HTTP_USER_AGENT"),
        )
        return self.get_response(request)