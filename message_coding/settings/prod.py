from __future__ import absolute_import

from .common import *

DEV = False
DEBUG_TEMPLATE = DEBUG

COMPRESS_ENABLED = get_env_setting('COMPRESS_ENABLED', True, type=bool)
COMPRESS_OFFLINE = get_env_setting('COMPRESS_OFFLINE', True, type=bool)

ALLOWED_HOSTS = get_env_setting("ALLOWED_HOSTS", 'localhost').split(',')
