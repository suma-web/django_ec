import base64
from django.http import HttpResponse

USERNAME = "admin"
PASSWORD = "pw"


class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/manage/"):
            auth = request.META.get("HTTP_AUTHORIZATION")

            if auth is None:
                return self._unauthorized()

            try:
                method, encoded = auth.split(" ")
                decoded = base64.b64decode(encoded).decode()
                username, password = decoded.split(":")
            except Exception:
                return self._unauthorized()

            if username != USERNAME or password != PASSWORD:
                return self._unauthorized()

        return self.get_response(request)

    def _unauthorized(self):
        response = HttpResponse(status=401)
        response["WWW-Authenticate"] = 'Basic realm="Manage Area"'
        return response
