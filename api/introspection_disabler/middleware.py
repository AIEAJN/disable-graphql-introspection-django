from django.http import JsonResponse
import json
from .models import AppConfig


class IntrospectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        config = AppConfig.objects.get(id=1)
        if not config.allow_introspection:
            if request.method == "POST" and request.content_type == "application/json":
                body = json.loads(request.body.decode("utf-8"))
                if "query" in body and "__schema" in body["query"]:
                    return JsonResponse(
                        {"message": "Introspection is not allowed!"}, status=400
                    )

        return self.get_response(request)   