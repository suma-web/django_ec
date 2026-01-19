from django.http import HttpResponse
import base64
import os

def basic_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        auth = request.META.get("HTTP_AUTHORIZATION")
        if auth:
            method, credentials = auth.split(" ", 1)
            if method.lower() == "basic":
                decoded = base64.b64decode(credentials).decode("utf-8")
                username, password = decoded.split(":", 1)

                if (
                    username == os.environ.get("BASIC_AUTH_USER")
                    and password == os.environ.get("BASIC_AUTH_PASSWORD")
                ):
                    return view_func(request, *args, **kwargs)

        response = HttpResponse(status=401)
        response["WWW-Authenticate"] = 'Basic realm="Restricted Area"'
        return response

    return wrapper
