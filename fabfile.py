"""
Define common admin and maintenance tasks here.
For more info: http://docs.fabfile.org/en/latest/
"""

from path import path
from fabric.api import run, env, prefix, quiet

from mbcore import conf
from mbcore.fabutils import factories, utils as _utils
from mbcore.fabutils.tasks import *


PROJECT_ROOT = path(__file__).abspath().realpath().dirname()
conf.configure(PROJECT_ROOT, 'message_coding')

# A dependencies management task
pip_requirements = {
    'dev': ('-r requirements/local.txt',),
    'prod': ('-r requirements/prod.txt',),
    'test': ('-r requirements/test.txt',),
}

pip_install = factories.pip_install_task(pip_requirements, default_env='dev')

def dependencies(default_env='dev'):
    """Install requirements for pip, npm, and bower all at once."""
    pip_install(default_env)
    npm_install()
    bower_install()

test = factories.test_task(default_settings='message_coding.settings.test')
test_coverage = factories.coverage_task(default_settings='message_coding.settings.test')

test_data_path = conf.PROJECT_ROOT / 'setup' / 'fixtures' / 'test_data.json'
make_test_data = factories.make_test_data_task(('base', 'api', 'project',
                                                'dataset', 'coding',
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

    denv = _utils.dot_env()

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

