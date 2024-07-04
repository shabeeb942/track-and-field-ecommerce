from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-0wt*jv91-f@7juzokz^8oc6!lo6-c%y6=lm51or&+8twg8e0rc")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]


INSTALLED_PLUGINS = [
    "tinymce",
    "registration",
    "crispy_forms",
    "crispy_bootstrap5",
    'easy_thumbnails',
    'django_filters',
    'import_export',
    'django_tables2',
    "compressor",
]

DJANGO_APPS = [
     "admin_interface",
    "colorfield",
    'django.contrib.admin',
    "django.contrib.humanize",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
     # "user_sessions",
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MODULES = [
    "web",
    "product",
    "accounts",
    "core",
    "order",
]

INSTALLED_APPS = INSTALLED_PLUGINS + DJANGO_APPS + MODULES

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trackandfield.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "web.context_processors.main_context",
            ],
        },
    },
]

WSGI_APPLICATION = 'trackandfield.wsgi.application'


# Define DATABASES (postgres-production)
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": "5432",
        'OPTIONS': {},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_L10N = True
USE_TZ = True


USE_L10N = False
DATE_INPUT_FORMATS = (
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d/%m/%y",
    "%d %b %Y",
    "%d %b, %Y",
    "%d %b %Y",
    "%d %b, %Y",
    "%d %B, %Y",
    "%d %B %Y",
)
DATETIME_INPUT_FORMATS = (
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M",
    "%d/%m/%y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

THUMBNAIL_ALIASES = {"": {"small": {"size": (300, 300), "crop": True},"extra_small":{"size": (200, 200), "crop": True}, "medium": {"size": (800, 1200), "crop": False},"banner": {"size": (1660, 430), "crop": True}}}
THUMBNAIL_BASEDIR = "thumbnails"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
STATIC_FILE_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = ((BASE_DIR / "static"),)
STATIC_ROOT = BASE_DIR / "assets"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

REGISTRATION_OPEN = True
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

#This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTH_USER_MODEL = "accounts.User"

SESSION_COOKIE_SECURE = True
DOMAIN = "http://127.0.0.1:8000"
# DOMAIN = "https://trackandfield.geany.website"

RAZOR_PAY_KEY = config("RAZOR_PAY_KEY")
RAZOR_PAY_SECRET = config("RAZOR_PAY_SECRET")

APP_SETTINGS = {
    "logo": "/static/dashboard/app/config/logo.png",
    "logo_mini": "/static/dashboard/app/config/logo.png",
    "favicon": "/static/dashboard/app/config/logo.png",
    "site_name": "Track & Field",
    "site_title": "Track & Field",
    "site_description": "Track & Field",
    "site_keywords": " Household Appliances and Electrical and Electronic Goods Merchant Wholesalers ,  Paper and Paper Product Merchant Wholesalers ,  Merchant Wholesalers, Durable Goods ,  Wholesale Trade ,  Electric household appliances, Track & Field",
    # "background_image": "/static/dashboard/app/config/background.jpg",
}
