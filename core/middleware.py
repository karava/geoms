# core/middleware.py
from django.http import HttpResponsePermanentRedirect

CANONICAL_HOST = "www.infratex.com.au"          # ← change if you prefer apex

class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]  # strip port if any
        if host != CANONICAL_HOST:
            new_url = f"https://{CANONICAL_HOST}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(new_url)  # 301
        return self.get_response(request)