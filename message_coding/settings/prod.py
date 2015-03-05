from __future__ import absolute_import

from .common import *

DEV = False

DEBUG = bool(get_env_setting('DEBUG', False))
DEBUG_TEMPLATE = DEBUG

COMPRESS_ENABLED = bool(get_env_setting('COMPRESS_ENABLED', True))
COMPRESS_OFFLINE = bool(get_env_setting('COMPRESS_OFFLINE', True))

ALLOWED_HOSTS = get_env_setting("ALLOWED_HOSTS", 'localhost').split(',')
