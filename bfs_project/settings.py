"""
Django settings for bfs_project project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
MEDIA_DIR = os.path.join(BASE_DIR, "media")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "l(p1)k6rv%d=6pv0cyazwli*ps21r4+&4%d+ka57%-z9yx_vkl"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*", "feedback360.bmsit.ac.in"]

AUTH_USER_MODEL = "general.User"
# Application definition

INSTALLED_APPS = [
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.general",
    "apps.feedback",
    "apps.django_chatterbot",
    "import_export",
    "apps",
    'widget_tweaks',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bfs_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "bfs_project.wsgi.application"

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/main"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "feedback",
        "USER": "postgres",
        "PASSWORD": "feedback321",
        "HOST": "13.232.62.217",
        "PORT": "5432",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

"""
Email settings
"""
EMAIL_HOST = "email-smtp.eu-west-1.amazonaws.com"
DEFAULT_FROM_EMAIL = "feedback@bmsit.ac.in"
EMAIL_PORT = 587
EMAIL_HOST_USER = "AKIA5TXBET4HAKGJLMC3"
EMAIL_HOST_PASSWORD = "BIdSZOxIofpOtLbFv1TOx9Mek/Wyd5MdSalOXu9+CRpA"
EMAIL_USE_TLS = True


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
STATICFILES_DIRS = [STATIC_DIR]
CORPUS_DIR = os.path.join(BASE_DIR, "corpus/")


# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = MEDIA_DIR


CHATTERBOT = {
    "name": "DevX Bot",
    "logic_adapters": [
        {
            "import_path": "chatterbot.logic.LowConfidenceAdapter",
            "threshold": 0.65,
            "default_response": "I am sorry, but I do not understand.",
        },
        {"import_path": "chatterbot.logic.BestMatch"},
        {
            "import_path": "apps.django_chatterbot.logic.profanity_adapter.ProfanityAdapter"
        },
        {"import_path": "apps.django_chatterbot.logic.user_adapter.UserAdapter"},
    ],
    "trainer": "chatterbot.trainers.ChatterBotCorpusTrainer",
    "training_data": [
        "corpus.feedback",
        "corpus.ai",
        "corpus.compliments",
        "corpus.botprofile",
        "chatterbot.corpus.english.greetings",
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.humor",
        "chatterbot.corpus.english.trivia",
        "chatterbot.corpus.english.history",
        "chatterbot.corpus.english.science",
        "chatterbot.corpus.english.movies",
        "chatterbot.corpus.english.psychology",
        "chatterbot.corpus.english.emotion",
        "chatterbot.corpus.english.computers",
    ],
}

ABUSE_FILE = os.path.join(CORPUS_DIR, "abuse.txt")
