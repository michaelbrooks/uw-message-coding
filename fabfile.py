"""
Define common admin and maintenance tasks here.
For more info: http://docs.fabfile.org/en/latest/
"""

import sys

from path import path
from fabric.api import run, env, prefix, quiet


PROJECT_ROOT = path(__file__).abspath().realpath().dirname()
sys.path.append(PROJECT_ROOT / 'setup')

from fabutils import conf

conf.configure(PROJECT_ROOT, 'message_coding')

from fabutils import factories
from fabutils.tasks import *


# A dependencies management task
dependencies = factories.dependencies_task(
    {
        'dev': ('-r requirements/local.txt',),
        'prod': ('-r requirements/prod.txt',),
        'test': ('-r requirements/test.txt',),
    },
    default_env='dev'
)

test = factories.test_task(default_settings='message_coding.settings.test')
test_coverage = factories.coverage_task(default_settings='message_coding.settings.test')

test_data_path = conf.PROJECT_ROOT / 'setup' / 'fixtures' / 'test_data.json'
make_test_data = factories.make_test_data_task(('base', 'api', 'corpus',
                                                'dimensions', 'datatable',
                                                'importer', 'enhance', 'questions',
                                                'auth', '--exclude=auth.Permission'),
                                               test_data_path)
load_test_data = factories.load_test_data_task(test_data_path)

def reset_dev(pull=None):
    """
    Fully update the development environment.
    This is useful after a major update.

    Runs reset_db, installs dependencies, migrate, load_test_data, and clear_cache.
    """
    print "\n"
    reset_db()

    if pull is not None:
        print "\n"
        pull()

    print "\n"
    dependencies()

    print "\n"
    migrate()

    print "\n"
    load_test_data()

    print "\n"
    clear_cache()


def deploy():
    """
    SSH into a remote server, run commands to update deployment,
    and start the server.
    
    This requires that the server is already running a 
    fairly recent copy of the code.

    Furthermore, the app must use a
    """

    denv = fabutils.dot_env()

    host = denv.get('DEPLOY_HOST', None)
    virtualenv = denv.get('DEPLOY_VIRTUALENV', None)

    if host is None:
        print red("No DEPLOY_HOST in .env file")
        return
    if virtualenv is None:
        print red("No DEPLOY_VIRTUALENV in .env file")
        return

    env.host_string = host

    with prefix('workon %s' % virtualenv):

        # Check prereqs
        with quiet():
            pips = run('pip freeze')
            if "Fabric" not in pips or 'path.py' not in pips:
                print green("Installing Fabric...")
                run('pip install Fabric path.py')

        run('fab pull')
        run('fab dependencies:prod')
        run('fab print_env check_database migrate')
        run('fab build_static restart_webserver')

