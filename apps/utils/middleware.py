from datetime import datetime
import logging

from django.conf import settings
from django.db import connection
from django.http import HttpRequest
from django.utils import timezone

LOGGER = logging.getLogger("app")


class PerformanceLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.UNLEASH_CLIENT.is_enabled("query_counter"):
            return self.get_response(request)

        start_time = timezone.now()

        response = self.get_response(request)

        end_time = timezone.now()
        self._log_query_times(request, start_time, end_time)

        return response

    @staticmethod
    def _log_query_times(request: HttpRequest, request_start_time: datetime, request_end_time: datetime) -> None:
        msg_parts = ["REQUEST PERFORMANCE STATS"]
        try:
            # Step 1: Request handling time
            request_time = request_end_time - request_start_time
            msg_parts.append(f"Request time (s): {request_time.total_seconds():.3f}")

            # Step 2: Query times
            query_times = [query["time"] for query in connection.queries] if connection else []
            query_times_joined = ",".join(query_times)
            msg_parts.append(f"Query times (s): {query_times_joined}")
            total_query_time = sum([float(query_time) for query_time in query_times])
            msg_parts.append(f"Total query time (s): {total_query_time:.3f}")

            # Step 3: Request info
            method = getattr(request, "method", "")
            path = getattr(request, "path", "")
            user = getattr(request, "user", "anonymous")
            msg_parts.append(f"Request info: {method} {path} by user {user}")

        except Exception as ex:  # noqa: B902
            # Being extra careful here, cannot avoid any instabilities
            # as this code runs on every request and is not essential.
            msg_parts.append(str(ex))

        LOGGER.info(" ".join(msg_parts))
