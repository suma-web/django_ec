import base64
import os
from django.http import HttpResponse
from django.conf import settings


def basic_auth_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if auth_header:
            try:
                auth_type, encoded = auth_header.split(" ", 1)
                if auth_type.lower() == "basic":
                    decoded = base64.b64decode(encoded).decode("utf-8")
                    username, password = decoded.split(":", 1)
                    if (
                        username == os.environ.get("BASIC_AUTH_USER")
                        and password == os.environ.get("BASIC_AUTH_PASSWORD")
                    ):
                        return view_func(request, *args, **kwargs)
            except Exception:
                pass

        response = HttpResponse(status=401)
        response["WWW-Authenticate"] = 'Basic realm="Management Area"'
        return response

    return _wrapped_view
