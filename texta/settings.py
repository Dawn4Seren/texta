######################### TEXTA Configuration File ########################

# This file contains all the framework's general configurable options which
# don't need changes in the source code. Some configurations are hardcoded
# into different applications' source code and may be altered to fine-tune
# the output or calculation results. For all hardcoded configurations,
# consult #TODO.
#
# Default configuration suffices for running a development version. For
# production, one needs to define server specific paths.
#
# General options define file and URL paths, #TODO
#
# Installation is covered in documentation at #TODO
#

from time import strftime
import json
import ast
import os

# Path to TEXTA's root directory. It is used in other paths as a prefix.
# BASE_DIR = os.path.realpath(os.path.dirname(__file__)) tries to determine
# the path programmatically but may occasionally fail.
#
BASE_DIR = os.path.realpath(os.path.dirname(__file__))

# When this is true, the scoro_preprocessor is enabled
#
SCORO_PREPROCESSOR_ENABLED = os.getenv('TEXTA_SCORO_PREPROCESSOR_ENABLED', False)
SCORO_PREPROCESSOR_ENABLED = ast.literal_eval(str(SCORO_PREPROCESSOR_ENABLED))

# When this is true, the paasteamet_preprocessor is enabled
PAASTEAMET_PREPROCESSOR_ENABLED = os.getenv('TEXTA_PAASTEAMET_PREPROCESSOR_ENABLED', False)
PAASTEAMET_PREPROCESSOR_ENABLED = ast.literal_eval(str(PAASTEAMET_PREPROCESSOR_ENABLED))


# When this is true, email confirmation is enabled
#
REQUIRE_EMAIL_CONFIRMATION = False

# Email settings
#
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'emailaddress@gmail.com'
EMAIL_HOST_PASSWORD = 'hunter2'
EMAIL_PORT = 587

############################ Server Type ###########################

# Server type allows to predetermine a wide range of options.
# It is used to switch between 'development' and 'production' instances,
# so that after setting up the variables, one only has to alter the
# SERVER_TYPE string to have a fully configured and functional instance.
#
# The default development version is tuned for hosting TEXTA locally and
# needs no further configuration. However, if your development version is
# on a remote machine, consult 'production' settings.
#
# URL_PREFIX_DOMAIN - domain address of the hosting server.
# URL_PREFIX_RESOURCE - resource which is responsible for hosting TEXTA
#                       application server.
# ROOT_URLCONF - Django's root urls.py file's package path.
# STATIC_URL - static directory's address.
# STATIC_ROOT - static directory's file path.
# DEBUG - whether to display verbose variable values and stack trace when
#         error occurs during page resolving.

STATIC_ROOT = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'static')
SERVER_TYPE = os.getenv('TEXTA_SERVER_TYPE')

if SERVER_TYPE is None:
	SERVER_TYPE = os.getenv('TEXTA_SERVER_TYPE', 'development')

if SERVER_TYPE == 'development':
	PROTOCOL = '{0}://'.format(os.getenv('TEXTA_PROTOCOL', 'http'))
	DOMAIN = os.getenv('TEXTA_DOMAIN', 'localhost')
	PORT = '8000'

	URL_PREFIX_DOMAIN = '{0}{1}:{2}'.format(PROTOCOL, DOMAIN, PORT)
	URL_PREFIX_RESOURCE = ''
	ROOT_URLCONF = 'texta.urls'
	STATIC_URL = URL_PREFIX_DOMAIN + '/static/'
	DEBUG = True

elif SERVER_TYPE == 'production':
	PROTOCOL = '{0}://'.format(os.getenv('TEXTA_PROTOCOL', 'http'))
	DOMAIN = os.getenv('TEXTA_DOMAIN', 'dev.texta.ee')

	URL_PREFIX_DOMAIN = '{0}{1}'.format(PROTOCOL, DOMAIN)
	URL_PREFIX_RESOURCE = ''
	ROOT_URLCONF = 'texta.urls'
	STATIC_URL = URL_PREFIX_DOMAIN + '/static/'
	DEBUG = False

elif SERVER_TYPE == 'docker':
	PROTOCOL = '{0}://'.format(os.getenv('TEXTA_PROTOCOL'))
	DOMAIN = os.getenv('TEXTA_HOST', 'localhost')
	PORT = os.getenv('TEXTA_PORT', None)
	URL_PREFIX_RESOURCE = os.getenv('TEXTA_PREFIX_RESOURCE', '')

	if PORT:
		URL_PREFIX_DOMAIN = '{0}{1}:{2}'.format(PROTOCOL, DOMAIN, PORT)
	else:
		URL_PREFIX_DOMAIN = '{0}{1}'.format(PROTOCOL, DOMAIN)

	ROOT_URLCONF = 'texta.urls'
	STATIC_URL = '/static/'
	DEBUG = True

########################### URLs and paths ###########################

# Defines URLs and paths which are used by various apps.

# URL to TEXTA's root. E.g. 'http://textadev.stacc.ee' or 'http://www.stacc.ee/texta'.
# Should not be altered.
#
URL_PREFIX = URL_PREFIX_DOMAIN + URL_PREFIX_RESOURCE

# URL to the application's login page. TEXTA's login page is its index page.
# Should not be altered. Needed for Django's auth module, used for redirecting
# when unauthorized user is attempting to access authorized content.
#
LOGIN_URL = URL_PREFIX

# Path to media files root directory.
#
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
PROTECTED_MEDIA = os.path.join(MEDIA_ROOT, 'protected_media')

# URL to media files root.
#
MEDIA_URL = 'files/'
ADMIN_MEDIA_PREFIX = '/media/'

# Path to users' visited words in Lex Miner.
#
USER_MODELS = os.path.join(BASE_DIR, 'data', 'usermodels')

# Path to users' language models.
#
MODELS_DIR = os.path.join(BASE_DIR, 'data', 'models')

# Path to Sven's projects
#
SCRIPT_MANAGER_DIR = os.path.join(MEDIA_ROOT, 'script_manager')

if not os.path.exists(MODELS_DIR):
	os.makedirs(MODELS_DIR)

if not os.path.exists(PROTECTED_MEDIA):
	os.makedirs(PROTECTED_MEDIA)

if not os.path.exists(SCRIPT_MANAGER_DIR):
	os.makedirs(SCRIPT_MANAGER_DIR)

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Avoid errors when sending too big files through the importer API.
# Increased vulnerability to DDoS attacks.
DATA_UPLOAD_MAX_MEMORY_SIZE = os.getenv('DJANGO_DATA_UPLOAD_MAX_MEMORY_SIZE', None)
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# New user are created as activated or deactivated (in which case superuser has to activate them manually)
USER_ISACTIVE_DEFAULT = os.getenv('TEXTA_USER_ISACTIVE_DEFAULT')
if USER_ISACTIVE_DEFAULT is None:
	USER_ISACTIVE_DEFAULT = True
else:
	USER_ISACTIVE_DEFAULT = json.loads(USER_ISACTIVE_DEFAULT.lower())

# Defines whether added datasets are 'public' or 'private'. Public datasets are accessible by all the existing users and
# new users alike. Access from a specific user can be revoked. Private datasets are not accessible by default, but
# access privilege can be granted.
DATASET_ACCESS_DEFAULT = 'private'

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# List of all host headers which are accepted to prevent host header poisoning.
# Should be altered if hosted on a remote machine.
#
ALLOWED_HOSTS = ['*']

# Defines which database backend does the application use. TEXTA uses only default with sqlite engine.
# Can change engine and database info as one sees fit.
#
DATABASES = {
	'default': {
		'ENGINE':       os.getenv('DJANGO_DATABASE_ENGINE', 'django.db.backends.sqlite3'),
		'NAME':         os.getenv('DJANGO_DATABASE_NAME', os.path.join(BASE_DIR, 'database', 'lex.db')),
		'USER':         os.getenv('DJANGO_DATABASE_USER', ''),  # Not used with sqlite3.
		'PASSWORD':     os.getenv('DJANGO_DATABASE_PASSWORD', ''),  # Not used with sqlite3.
		'HOST':         os.getenv('DJANGO_DATABASE_HOST', ''),
		# Set to empty string for localhost. Not used with sqlite3.
		'PORT':         os.getenv('DJANGO_DATABASE_PORT', ''),
		# Set to empty string for default. Not used with sqlite3.
		'BACKUP_COUNT': 5,
		'CONN_MAX_AGE': None
	}
}

if SERVER_TYPE == 'development':
	if not os.path.exists(os.path.dirname(DATABASES['default']['NAME'])) and os.environ.get('DJANGO_DATABASE_NAME') is None:
		os.makedirs(os.path.dirname(DATABASES['default']['NAME']))

TIME_ZONE = 'Europe/Tallinn'
LANGUAGE_CODE = 'et'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

# Key used for seed in various Django's features needing crypto or hashing.
#
SECRET_KEY = '+$18(*8p_h0u6-)z&zu^@=$2h@=8qe+3uwyv+3#v9*)fy9hy&f'

# Defines template engine and context processors to render dynamic HTML pages.
#
TEMPLATES = [
	{
		'BACKEND':  'django.template.backends.django.DjangoTemplates',
		'DIRS':     [],
		'APP_DIRS': True,
		'OPTIONS':  {
			'context_processors': [
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.debug',
				'django.template.context_processors.i18n',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
				'django.template.context_processors.tz',
				'django.template.context_processors.request',
				'django.contrib.messages.context_processors.messages',
				'utils.context_processors.get_version'
			],
			#               'loaders': [
			#                'django.template.loaders.filesystem.Loader',
			#                'django.template.loaders.app_directories.Loader',
			#            ],
			'debug':              DEBUG,
		},
	},
]

# List of Django plugins used in TEXTA.
#

MIDDLEWARE = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'texta.ExceptionHandlerMiddleware.ExceptionHandlerMiddleware'
)

# List of built-in and custom apps in use.
#
INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',
	'django.contrib.staticfiles',
	'lexicon_miner',
	'conceptualiser',
	'mwe_miner',
	'account',
	'searcher',
	'ontology_viewer',
	'base',
	'permission_admin',
	'grammar_builder',
	'search_api',
	'dataset_importer',
	'importer_api',
	'task_manager',
	'rest_framework',
)

############################ Elasticsearch ###########################

# Elasticsearch connection settings. Elasticsearch is used throughout
# TEXTA to store the analyzed documents.
#


# Elasticsearch URL with protocol specification. Can be either localhost
# or remote address ex: http://elastic-dev.texta.ee:9200.
es_url = os.getenv('TEXTA_ELASTICSEARCH_URL', 'http://localhost:9200')

es_prefix = os.getenv('TEXTA_ELASTICSEARCH_PREFIX', '')

# Elasticsearch links to outside world
# ('index_name','mapping_name','field_name'):('url_prefix','url_suffix')
es_links = {
	('etsa_new', 'event_dgn', 'epiId'): ('https://p12.stacc.ee/common/epicrisis/?id=', ''),
	('etsa_new', 'event_dgn', 'patId'): ('https://p12.stacc.ee/common/aegread/index.php/aegrida/get/?id=', '')
}


# Date format used in Elasticsearch fields.
#
es_date_format = 'yyyy-MM-dd'

# Python date format
#
date_format = '%Y-%m-%d'

# Set to True if Elasticsearch needs authentication. Tested with basic auth.
es_use_ldap = False
es_ldap_user = os.getenv('TEXTA_LDAP_USER')
es_ldap_password = os.getenv('TEXTA_LDAP_PASSWORD')

# Get MLP URL from environment
MLP_URL = os.getenv('TEXTA_MLP_URL', 'http://localhost:5000')

# Dataset Importer global parameters
DATASET_IMPORTER = {
	'directory':          os.path.join(BASE_DIR, 'files', 'dataset_importer'),
	'import_processes':   2,
	'process_batch_size': 1000,
	'sync':               {
		'enabled':             False,
		'interval_in_seconds': 10,
		'index_sqlite_path':   os.path.join(BASE_DIR, 'database', 'import_sync.db')
	}
}

if not os.path.exists(DATASET_IMPORTER['directory']):
	os.makedirs(DATASET_IMPORTER['directory'])


############################### Logging ##############################

# Path to the log directory. Default is /log
LOG_PATH = os.path.join(BASE_DIR, 'log')

# Separator used to join different logged features.
LOGGING_SEPARATOR = ' - '

# Paths to info and error log files.
INFO_LOG_FILE_NAME = os.path.join(LOG_PATH, "info.log")
ERROR_LOG_FILE_NAME = os.path.join(LOG_PATH, "error.log")
MIGRATION_LOG_FILE_NAME = os.path.join(LOG_PATH, "migration.log")

# Logger IDs, used in apps. Do not change.
INFO_LOGGER = 'info_logger'
ERROR_LOGGER = 'error_logger'
MIGRATION_LOGGER = 'migration_logger'

USING_GRAYLOG = os.getenv("USING_GRAYLOG", False)
GRAYLOG_HOST_NAME = os.getenv("GRAYLOG_HOST_NAME", "localhost")
GRAYLOG_PORT = int(os.getenv("GRAYLOG_PORT", 12201))

# Most of the following logging settings can be changed.
# Especially format, logging levels, logging class and filenames.
LOGGING = {
	'version':                  1,
	'disable_existing_loggers': False,
	'filters': {
		'require_graylog_instance': {
			'()': 'texta.logger_handler.RequireGraylogInstance'
		}
	},

	'formatters':               {
		'detailed':       {
			'format': LOGGING_SEPARATOR.join(['%(levelname)s', '%(module)s', 'function: %(funcName)s', 'line: %(lineno)s', '%(name)s', 'PID: %(process)d', 'TID: %(thread)d', '%(message)s', '%(asctime)-15s']),
			'()': 'pythonjsonlogger.jsonlogger.JsonFormatter',

		},
		'normal':         {
			'format': LOGGING_SEPARATOR.join(['%(levelname)s', '%(module)s', '%(message)s', '%(asctime)s'])
		},
		'detailed_error': {
			'format': '\n' + LOGGING_SEPARATOR.join(['%(levelname)s', '%(module)s', '%(name)s', 'PID: %(process)d', 'TID: %(thread)d', '%(funcName)s', '%(message)s', '%(asctime)-15s'])
		},
	},

	'handlers':                 {
		'graypy': {
			'level': 'DEBUG',
			'class': 'graypy.GELFUDPHandler',
			'host': GRAYLOG_HOST_NAME,
			'port': GRAYLOG_PORT,
			'filters': ['require_graylog_instance']
		},

		'info_file':             {
			'level':     'INFO',
			'class':     'logging.FileHandler',
			'formatter': 'detailed',
			'filename':  INFO_LOG_FILE_NAME,
			'encoding':  'utf8',
			'mode':      'a'
		},
		'error_file':            {
			'level':     'ERROR',
			'class':     'logging.FileHandler',
			'formatter': 'detailed_error',
			'filename':  ERROR_LOG_FILE_NAME,
			'encoding':  'utf8',
			'mode':      'a',
		},
		'migration_file':            {
			'level':     'INFO',
			'class':     'logging.FileHandler',
			'formatter': 'detailed',
			'filename':  MIGRATION_LOG_FILE_NAME,
			'encoding':  'utf8',
			'mode':      'a',
		},

		'console':    {
			'level':     'INFO',
			'class':     'logging.StreamHandler',
			'formatter': 'detailed',
		},
	},

	'loggers':                  {
		INFO_LOGGER:     {
			'level':    'INFO',
			'handlers': ['info_file', 'graypy'],
			'propagate': True
		},
		ERROR_LOGGER:    {
			'level':    'ERROR',
			'handlers': ['console', 'error_file', 'graypy']
		},
		MIGRATION_LOGGER:    {
			'level':    'INFO',
			'handlers': ['console', 'migration_file', 'graypy']
		},

		# Big parent of all the Django loggers, MOST (not all) of this will get overwritten.
		# https://docs.djangoproject.com/en/2.1/topics/logging/#topic-logging-parts-loggers
		'django':        {
			'handlers':  ['console', 'error_file', 'graypy'],
			'level':     'ERROR',
		},

		# Log messages related to the handling of requests.
		# 5XX responses are raised as ERROR messages; 4XX responses are raised as WARNING messages
		'django.request': {
			'handlers':  ['error_file', 'error_file', 'graypy'],
			'level':     'ERROR',
			'propagate': False,
		},

		# Log messages related to the handling of requests received by the server invoked by the runserver command.
		# HTTP 5XX responses are logged as ERROR messages, 4XX responses are logged as WARNING messages,
		# everything else is logged as INFO.
		'django.server': {
			'handlers':  ['console', 'graypy'],
			'level':     'ERROR',
			'propagate': False,
		}

	}
}

# TEXTA Facts structure
FACT_PROPERTIES = {
	'type':       'nested',
	'properties': {
		'doc_path': {'type': 'keyword'},
		'fact':     {'type': 'keyword'},
		'num_val':  {'type': 'long'},
		'spans':    {'type': 'keyword'},
		'str_val':  {'type': 'keyword'}
	}
}

# Fact field name, use this instead of a magic string
FACT_FIELD = 'texta_facts'
LANGUAGE_CODE = "en"

############################ Boot scripts ###########################

# Several scripts ran during the boot to set up files and directories.
# Scripts will only be run if settings is imported from 'texta' directory, e.g. as a result of manager.py, or by Apache (user httpd / apache)

from utils.setup import write_navigation_file, ensure_dir_existence

write_navigation_file(URL_PREFIX, STATIC_URL, STATIC_ROOT)
ensure_dir_existence(LOG_PATH)
ensure_dir_existence(MODELS_DIR)
ensure_dir_existence(USER_MODELS)
