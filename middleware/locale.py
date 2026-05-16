from urllib.parse import parse_qs

from django.utils.translation import activate


class WebSocketLocaleMiddleware:
    """
    Middleware to handle i18n for WebSockets in Django Channels.
    It reads the 'lang' query parameter or the 'accept-language' header.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Try to get language from query string
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        lang = query_params.get("lang", [None])[0]

        # If not in query string, try accept-language header
        if not lang:
            headers = dict(scope.get("headers", []))
            accept_language = headers.get(b"accept-language", b"").decode("utf-8")
            if accept_language:
                # Naive parsing, takes the first language in the list
                lang = accept_language.split(",")[0].split(";")[0].strip()

        if lang:
            activate(lang)

        return await self.inner(scope, receive, send)
