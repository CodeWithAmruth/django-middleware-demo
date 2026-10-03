import time
from django.http import HttpResponse
from django.conf import settings


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request: {request.method} {request.path}")
        # print("Before")
        response = self.get_response(request)
        print(f"Response: {response.status_code} {response.reason_phrase}")
        # print("After")
        return response


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()

        response = self.get_response(request)

        duration = time.perf_counter() - start_time

        print(f"{request.method}{request.path} took {duration:.2f} seconds")

        return response


class AuthenticationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/private/"):

            if not request.user.is_authenticated:
                return HttpResponse(
                    "You must logged in to access this page.", status=401
                )

            # return self.get_response(request)

        return self.get_response(request)


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        maintenance_mode = getattr(settings, "MAINTENANCE_MODE", False)

        expempt_paths = getattr(settings, "MAINTENANCE_MODE_PATHS", [])
        print(f"Maintenance mode: {maintenance_mode}, Exempt paths: {expempt_paths}")

        if maintenance_mode:

            if request.path in expempt_paths:
                return HttpResponse(
                    "Maintenance mode is enabled. Please try again later.", status=503
                )

        return self.get_response(request)
