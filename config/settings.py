import os
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from .template import TEMPLATE_CONFIG, THEME_LAYOUT_DIR, THEME_VARIABLES

load_dotenv()  # Take environment variables from .env.

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", default='your-secret-key')  # Foydalanuvchi tomonidan belgilangan maxfiy kalit

DEBUG = os.environ.get("DEBUG", 'False').lower() in ['true', 'yes', '1']

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "webtest.namspi.uz", "e-manzil.namspi.uz"]

ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", default="local")

SPECIAL_APPS = [
    "auth.apps.AuthConfig",
    "accounts",
    "apps.data",
    "apps.e_manzil",
]

OTHER_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_jwt',  # Bu qatorni qo'shish
]

MAIN_APPS = [
    "other.dashboards",
    "other.layouts",
    "other.front_pages",
    "other.mail",
    "other.chat",
    "other.my_calendar",
    "other.kanban",
    "other.ecommerce",
    "other.academy",
    "other.logistics",
    "other.invoice",
    "other.users",
    "other.access",
    "other.pages",
    "other.authentication",
    "other.wizard_examples",
    "other.modal_examples",
    "other.cards",
    "other.ui",
    "other.extended_ui",
    "other.icons",
    "other.forms",
    "other.form_layouts",
    "other.form_wizard",
    "other.form_validation",
    "other.tables",
    "other.charts",
    "other.maps",
    "other.transactions",
]

INSTALLED_APPS = [
    'grappelli',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    *MAIN_APPS,
    *SPECIAL_APPS,
    *OTHER_APPS,
]

AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    'auth.custom_backend.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_BLACKLIST': 'rest_framework_simplejwt.token_blacklist',
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT tokenlar uchun
        'rest_framework.authentication.SessionAuthentication',  # Django sessiyalar uchun
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "web_project.language_middleware.DefaultLanguageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.language_code",
                "config.context_processors.my_setting",
                "config.context_processors.get_cookie",
                "config.context_processors.environment",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme",
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme",
            ],
        },
    },
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'https://webtest.namspi.uz',
    'https://e-manzil.namspi.uz',
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
    ("uz", _("Uzbek")),
    ("de", _("German")),
]

LANGUAGE_CODE = "en"

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "src" / "assets",
]

BASE_URL = os.environ.get("BASE_URL", default="http://127.0.0.1:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
TEMPLATE_CONFIG = TEMPLATE_CONFIG
THEME_VARIABLES = THEME_VARIABLES

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_AGE = 3600

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:5050",
    "https://webtest.namspi.uz",
    "https://e-manzil.namspi.uz"
]

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI_LOCAL")
AUTHORIZE_URL = os.getenv("AUTHORIZE_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
RESOURCE_OWNER_URL = os.getenv("RESOURCE_OWNER_URL")
