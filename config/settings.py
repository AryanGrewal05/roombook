import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "ci-only-not-a-secret")
DEBUG = False
ALLOWED_HOSTS = ["localhost", "testserver"]
ROOT_URLCONF = "config.urls"
INSTALLED_APPS = ["django_mongodb_backend", "rest_framework", "booking"]
DATABASES = {
    "default": {
        "ENGINE": "django_mongodb_backend",
        "HOST": os.environ.get("MONGODB_URI", "mongodb://localhost:27017"),
        "NAME": "roombook",
    }
}
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
DATABASE_ROUTERS = ["django_mongodb_backend.routers.MongoRouter"]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "UNAUTHENTICATED_USER": None,
}
USE_TZ = True
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Production-only hardening, switched on by the deploy environment.
if os.environ.get("DJANGO_SECURE") == "1":
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CSRF_COOKIE_SECURE = True
