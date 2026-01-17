from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from ipgeolocation import IpGeolocationAPI

from .models import RequestLog, BlockedIP

geo_api = IpGeolocationAPI(settings.IPGEOLOCATION_API_KEY)


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied")

        # Cache geolocation for 24 hours
        geo = cache.get(ip)
        if not geo:
            try:
                geo = geo_api.get_location(ip)
                cache.set(ip, geo, 60 * 60 * 24)
            except Exception:
                geo = {}

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo.get("country_name"),
            city=geo.get("city"),
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
