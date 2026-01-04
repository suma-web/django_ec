from django.http import HttpResponse
from functools import wraps
import base64

def basic_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if auth_header:
            try:
                auth_type, encoded = auth_header.split(" ", 1)
                if auth_type.lower() == "basic":
                    decoded = base64.b64decode(encoded).decode("utf-8")
                    username, password = decoded.split(":", 1)

                    if username == "admin" and password == "pw":
                        return view_func(request, *args, **kwargs)
            except Exception:
                pass

        response = HttpResponse("認証されていません", status=401)
        response["WWW-Authenticate"] = 'Basic realm="Management Area"'
        return response

    return _wrapped_view
