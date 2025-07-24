from datetime import timedelta

from .base import *

DEBUG = False

ADMINS = [
    ("Praise Idowu", "ifeoluwapraise02@gmail.com"),
]


ALLOWED_HOSTS = [".railway.app"]

DATABASE_URL = config("DATABASE_URL")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": config("POSTGRES_PORT"),
    }
}

if DATABASE_URL:
    import dj_database_url

    if DATABASE_URL.startswith("postgres://"):
        DATABASES["default"] = dj_database_url.config(
            conn_max_age=500,
            conn_health_checks=True,
        )

CELERY_BROKER_URL = "redis://redis:6379/1"

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 1

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=60
    ),  # Short-lived access tokens for production
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": config("JWT_SECRET_KEY"),
}

FRONTEND_URL = config("FRONTEND_URL_PROD")

CORS_ALLOWED_ORIGINS = [
    config("FRONTEND_URL_PROD"),
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    config("FRONTEND_URL_PROD"),
]

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)  # Fixed too many redirects
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
