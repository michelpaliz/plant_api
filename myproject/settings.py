import os
from pathlib import Path
import dj_database_url

# ✅ Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Load secret key from environment variable (important for security)
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-1^+&4#g9pfpz5_wvz5_wct!1vc3ms@!$a6#*x3#*fqf)%m@t9j",
)

# ✅ Set DEBUG mode from environment variable (False in production)
DEBUG = False  # Change from True to False in production

# ✅ Define allowed hosts (reads from environment or defaults)
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "plant-api-lyaj.onrender.com", "fastezcode.com"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "corsheaders",  # For CORS support
    "rest_framework",
    # Your app
    "myapp",
]

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ]
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Add CORS middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ✅ CORS Settings
# Use conditional settings for development vs production
if DEBUG:
    # In development, allow all origins
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # In production, control via an environment variable (default False)
    CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL", "False") == "True"

# Additionally, specify allowed origins (if not allowing all)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:7000",  # Local frontend (adjust port as needed)
    "https://fastezcode.com",  # Production frontend
]

# ✅ Root URL configuration
ROOT_URLCONF = "myproject.urls"

# ✅ Template settings
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

# ✅ WSGI application
WSGI_APPLICATION = "myproject.wsgi.application"

# ✅ Database settings (SQLite for local, PostgreSQL for production)
DATABASES = {
    "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3")
}

# ✅ Authentication password validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ✅ Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ✅ Static files settings (for deployment on Render)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Required for Render

# ✅ Media files settings
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ✅ Default auto primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
