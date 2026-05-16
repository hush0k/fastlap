import uuid
from collections.abc import Awaitable
from contextvars import ContextVar
from logging import Logger, getLogger
from typing import Callable

from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from django.http import HttpRequest, HttpResponse

logger: Logger = getLogger(__name__)

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse | Awaitable[HttpResponse]],
    ) -> None:
        self.get_response = get_response
        self.is_async = iscoroutinefunction(get_response)
        if self.is_async:
            markcoroutinefunction(self)

    def __call__(self, request: HttpRequest) -> HttpResponse | Awaitable[HttpResponse]:
        if self.is_async:
            return self.__acall__(request)

        request_id: str = str(uuid.uuid4())
        request_id_var.set(request_id)

        response: HttpResponse = self.get_response(request)
        response["X-Request-ID"] = request_id

        return response

    async def __acall__(self, request: HttpRequest) -> HttpResponse:
        request_id: str = str(uuid.uuid4())
        request_id_var.set(request_id)

        response: HttpResponse = await self.get_response(request)
        response["X-Request-ID"] = request_id

        return response


class RequestLoggingMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse | Awaitable[HttpResponse]],
    ) -> None:
        self.get_response = get_response
        self.is_async = iscoroutinefunction(get_response)
        if self.is_async:
            markcoroutinefunction(self)

    def __call__(self, request: HttpRequest) -> HttpResponse | Awaitable[HttpResponse]:
        logger.debug(
            '"%s %s" | %s | %s |',
            request.method,
            request.path,
            request.META.get("REMOTE_ADDR"),
            request.META.get("HTTP_USER_AGENT"),
        )
        if self.is_async:
            return self.__acall__(request)

        return self.get_response(request)

    async def __acall__(self, request: HttpRequest) -> HttpResponse:
        return await self.get_response(request)
