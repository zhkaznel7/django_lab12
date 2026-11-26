import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_flag(name):
    return os.getenv(name, "").strip().lower() in {"true", "1", "yes"}


def env_list(name):
    return [value.strip() for value in os.getenv(name, "").split(",") if value.strip()]


SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = env_flag("DEBUG")
ON_RENDER = env_flag("RENDER")
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if ON_RENDER and render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")

if ON_RENDER and not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000

INSTALLED_APPS = ["django.contrib.staticfiles", "tickets"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "config.middleware.ValidateHostMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
}]

database_url = os.getenv("DATABASE_URL")
if ON_RENDER and not database_url:
    raise ImproperlyConfigured("DATABASE_URL is required on Render.")
if database_url:
    database = dj_database_url.parse(database_url, conn_max_age=60, conn_health_checks=True)
else:
    database = {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
DATABASES = {"default": database}

LANGUAGE_CODE = "kk"
TIME_ZONE = "Asia/Qyzylorda"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"console": {"format": "{asctime} {levelname} {name} {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "console"}},
    "loggers": {
        "tickets": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.security.DisallowedHost": {
            "handlers": ["console"], "level": "ERROR", "propagate": False,
        },
    },
}
