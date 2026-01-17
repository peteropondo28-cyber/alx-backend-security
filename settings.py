INSTALLED_APPS += [
    "ip_tracking",
    "ratelimit",
]

MIDDLEWARE = [
    "ip_tracking.middleware.IPLoggingMiddleware",
    # other middleware...
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

IPGEOLOCATION_API_KEY = "your_api_key_here"
