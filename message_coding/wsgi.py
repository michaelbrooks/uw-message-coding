"""
WSGI config for {{ project_name }} project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
from path import path

# Make sure the project root is on the path
from path import path
PROJECT_ROOT = path(__file__).abspath().realpath().dirname().parent
sys.path.append(PROJECT_ROOT)

# Load the .env file
sys.path.append(PROJECT_ROOT / 'setup')
from fabutils import env_file
env_file.load(PROJECT_ROOT / '.env')

# Just in case that didn't do it...
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "message_coding.settings.prod")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
