# Django settings for giant project.
import os
from os.path import dirname
basedir = dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'giant',
        'USER': 'root',
        'PASSWORD': 'abirato',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-pe'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/media/' % basedir

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ah*xk6x76dg0-roz&(k&1qo9o)xsh4sm*z4gua2-gt)*!)4a)n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'svn.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % basedir
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.admin',
    # aplicaciones de giant
    'agentes',
    'clientes',
    'proyectos',
    'empresa',
    'admin',
    'common',
    # utilidades
    'sorl.thumbnail',
)

LOGIN_URL = '/admin/'

# Modelo para usuario
AUTH_PROFILE_MODULE = "common.Usuario"
API_GOOGLE = "ABQIAAAAMRdj9lILtQvXkiEUNZPsEBT3ZPJlF64cLZ5z26Oz-plJNAovGhRKEx2bnH1OpkIAMK_bQH_5WrO5kw"
# Opciones para el envio de emails desde el servidor
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'aqpnet'
EMAIL_HOST_PASSWORD = '04718802'
EMAIL_PORT = 587
#EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "aqpnet@mail.webfaction.com"
SERVER_EMAIL = "aqpnet@mail.webfaction.com"

# Opciones del cache
CACHE_BACKEND = 'db://cachetable/?timeout=30&max_entries=80'
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
