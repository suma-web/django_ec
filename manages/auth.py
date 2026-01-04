import base64
from django.http import HttpResponse


def basic_auth_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth = request.META.get("HTTP_AUTHORIZATION")

        if auth:
            try:
                method, credentials = auth.split(" ", 1)
                if method.lower() == "basic":
                    decoded = base64.b64decode(credentials).decode("utf-8")
                    username, password = decoded.split(":", 1)
                    if username == "admin" and password == "pw":
                        return view_func(request, *args, **kwargs)
            except Exception:
                pass

        response = HttpResponse("Unauthorized", status=401)
        response["WWW-Authenticate"] = 'Basic realm="Manage Area"'
        return response

    return _wrapped_view
