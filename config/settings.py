
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&swf-368$&fdjp+mp3@zmbk(d!bedry&ulm(sbwyqm&+p*#%94"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",


    # Apps
    "accounts.apps.AccountsConfig",
    "blog",
    "home",

    #tools
    'taggit',
    "django_ckeditor_5",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "fa-ir"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# Account and User Settings
AUTH_USER_MODEL = "accounts.User"


#Static and Media settings
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"




# CKEditor
CKEDITOR_5_CONFIGS = {
    'default': {
        'language': 'fa',
        'toolbar': [
            'undo', 'redo', '|',
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',

            'fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor', '|',

            'alignment', 'textDirection', '|',

            'bulletedList', 'numberedList', 'blockQuote', '|',

            'link', 'imageUpload', 'insertTable', 'horizontalLine', '|',

            'codeBlock', 'specialCharacters', '|',

            'fullScreen',
            'sourceEditing',
        ],

        'fontFamily': {
            'options': [
                'Default',
                'IRZar',
                'IRANSans',
                'Vazir',
                'Shabnam',
                'Sahel',
                'Tahoma',
                'Nazanin',
                'Yekan'
            ],
            'supportAllValues': True
        },

        'fontSize': {
            'options': [
                'default', 12, 14, 16, 18, 20, 22, 24, 26, 28, 32
            ],
            'supportAllValues': True
        },

        'alignment': {
            'options': ['left', 'right', 'center', 'justify']
        },

        'image': {
            'toolbar': [
                'imageStyle:inline',
                'imageStyle:block',
                'imageStyle:side',
                '|',
                'imageStyle:alignLeft',
                'imageStyle:alignRight',
                'imageStyle:full',
                '|',
                'imageTextAlternative'
            ],
            'styles': [
                'inline',
                'block',
                'side',
                'alignLeft',
                'alignRight',
                'full'
            ]
        },

        'table': {
            'contentToolbar': [
                'tableColumn',
                'tableRow',
                'mergeTableCells',
                'tableProperties',
                'tableCellProperties'
            ]
        },

        'height': 600,
        'isReadOnly': False,
    }
}

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

