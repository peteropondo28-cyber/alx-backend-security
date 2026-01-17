from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_anomalies():
    one_hour_ago = now() - timedelta(hours=1)

    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    ip_activity = {}

    for log in logs:
        ip_activity.setdefault(log.ip_address, []).append(log.path)

    for ip, paths in ip_activity.items():
        if len(paths) > 100 or any(p in ["/admin", "/login"] for p in paths):
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason="High request volume or sensitive path access",
            )
