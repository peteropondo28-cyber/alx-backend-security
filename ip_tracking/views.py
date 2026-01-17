from django.http import JsonResponse
from ratelimit.decorators import ratelimit


@ratelimit(key="ip", rate="10/m", method="ALL", block=True)
def authenticated_login_view(request):
    return JsonResponse({"message": "Authenticated login"})


@ratelimit(key="ip", rate="5/m", method="ALL", block=True)
def anonymous_login_view(request):
    return JsonResponse({"message": "Anonymous login"})
