from datetime import timedelta
from logging import getLogger
from pathlib import Path

from decouple import config
from dotenv import load_dotenv

logger = getLogger(__name__)

ENV_FILE = config("ENV_FILE", default=".env")
logger.warning(f"Using ENV_FILE={ENV_FILE}")

load_dotenv(ENV_FILE)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "axes",
    # Apps
    "apps.users",
    "apps.common",
    "apps.drivers",
    "apps.teams",
    "apps.news",
    "apps.race_tracks",
    "apps.tournaments",
    "apps.team_stuff",
    "apps.races",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "middleware.requests.RequestIDMiddleware",
    "middleware.requests.RequestLoggingMiddleware",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
    }
}

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "FastLap API",
    "DESCRIPTION": "API for motorsport fans platform",
    "VERSION": "1.0.0",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 0.5
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]
AXES_RESET_ON_SUCCESS = True
AXES_LOCK_OUT_AT_FAILURE = True


class MEDIA_LOCATION:
    # TODO: move /series/logo to /series/logos
    SERIES_LOGO: Path = Path("series/logo/")
    TOURNAMENTS_LOGO: Path = Path("tournaments/logos/")
    ARTICLE_COVERS: Path = Path("articles/covers/")
    DRIVER_PROFILE_IMAGE: Path = Path("drivers/profile_images")


ARTICLE_IMAGE_MAX_SIZE_MB = 10
ARTICLE_IMAGE_MAX_SIZE_BYTES = ARTICLE_IMAGE_MAX_SIZE_MB * 1024 * 1024
TOURNAMENT_LOGO_MAX_SIZE_MB = 20
TOURNAMENT_LOGO_MAX_SIZE_BYTES = TOURNAMENT_LOGO_MAX_SIZE_MB * 1024 * 1024

LOG_LEVEL = config("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} |{name:36s}|:{lineno:<4d} "
            "[{levelname:8s}] <{request_id:36s}> - {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname:8s}] - {message}",
            "style": "{",
        },
    },
    "filters": {
        "request_id": {
            "()": "config.logger.RequestIDFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "simple",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "apps": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "middleware": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "test": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

FIREBASE_PROJECT_ID = config("FIREBASE_PROJECT_ID", default="")
FIREBASE_COLLECTION_USERS = "users"
FIREBASE_COLLECTION_AVATARS = "avatars"
FIREBASE_CREDENTIALS_PATH = Path(config("FIREBASE_CREDENTIALS_PATH"))

if not FIREBASE_CREDENTIALS_PATH.is_absolute():
    FIREBASE_CREDENTIALS_PATH = BASE_DIR / FIREBASE_CREDENTIALS_PATH


AVATAR_MAX_SIZE_MB = 2
AVATAR_MAX_SIZE_BYTES = AVATAR_MAX_SIZE_MB * 1024 * 1024
ALLOWED_AVATAR_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
