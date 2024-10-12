import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '24q_*&tn+5k_*6h6$nsccghwwb#8b%v4i)1h(wd08_02_-(czt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
    },
}

# Application definition

INSTALLED_APPS = [
        'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Users.apps.UsersConfig',
    'wallet.apps.WalletConfig',
    'company.apps.CompanyConfig',
    'myadmin.apps.MyadminConfig',
    'core.apps.CoreConfig',
    'crispy_forms',

    # 3rd party
    'whitenoise.runserver_nostatic',

       #api
    'rest_framework',
    'rest_framework.authtoken',

]

CRISPY_TEMPLATE_PACK = 'bootstrap4'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'bulligon_signals.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'Users/templates'),
            os.path.join(BASE_DIR, 'core/templates'),
            os.path.join(BASE_DIR, 'core/templates/email'),
            os.path.join(BASE_DIR, 'templates/email'),
            os.path.join(BASE_DIR, 'templates/registration'),
            os.path.join(BASE_DIR, 'templates/admin dashboard'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'core.context.core',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bulligon_signals.wsgi.application'

AUTH_USER_MODEL = 'Users.User'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


if DEBUG :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            "OPTIONS": {
                "timeout": 30,
            }
        },
        "OPTIONS": {
        # ...
        "timeout": 30,
        # ...
    }
    }

else :
    # Replace the SQLite DATABASES configuration with PostgreSQL:
   
    """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bulligonsignals',
        'USER': 'arcticxpress',
        'PASSWORD': 'Wdbtdpe51sbQsroUeLrTFgvVOk3Qe5O1',
        'HOST': 'postgresql://arcticxpress:Wdbtdpe51sbQsroUeLrTFgvVOk3Qe5O1@dpg-cqcne9tumphs73fhfmeg-a/arcticxpress',
        'PORT': '5432',  # Default PostgreSQL port
    }
    """
    DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost:5432/mydatabase')
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [ 

    os.path.join(BASE_DIR, "static")
]

SITE_NAME = ""

STATIC_ROOT = os.path.join(BASE_DIR, "asset")

STATIC_URL = '/static/'     
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


LOGIN_REDIRECT_URL = 'login-redirect'

LOGOUT_REDIRECT_URL = 'index'
STATIC_URL = '/static/'

# EMAIL FOR ZOHO 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.eu'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# for other emails
PRIMARY_EMAIL_ZOHO = "bulligonsignals@gmail.com"
EMAIL_HOST_USER_SUPPORT = "customer.support@bulligonsignals.com"
EMAIL_HOST_USER_TRANSACTION = "transaction@bulligonsignals.com"
DEFAULT_FROM_EMAIL = "support@bulligonsignals.com"
EMAIL_HOST_PASSWORD = 'Y6li9p@Poko'
EMAIL_HOST_USER_ALERT = "transaction@bulligonsignals.com"

#EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
#EMAIL_FILE_PATH =  os.path.join(BASE_DIR, "sent-emails")


EMAIL_USE_TLS = True

SITE_NAME = "Bulligon Signals"
SITE_ADDRESS = "https://www.bulligonsignals.com/"

FREE_PLAN_DURATION = 2  # in days
SUBSCRIPTION_DURATION = 365  # in days


#TAWKTO
EMAIL = "Sleykesh22@gmail.com"
PASSWORD = "Y6li9p@Poko" 




REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES' : [
        #"rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ]

}

#CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_ALL_ORIGINS = True

"""CORS_ALLOW_METHODS = [
    "GET"
]"""


DEFAULT_AUTO_FIELD='django.db.models.AutoField'



JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Bulligon Signals Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Bulligon Signals",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Bulligon Signals",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "img/logo/logo-name.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "img/logo/icon-jazz.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "img/logo/logo-name-dark.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": ["logo"],

    "custom_css": "css/style.css",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "img/logo/icon-jazz.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome Admin!",

    # Copyright on the footer
    "copyright": "Bulligon Signals",
}
