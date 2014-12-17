"""
Define common admin and maintenance tasks here.
For more info: http://docs.fabfile.org/en/latest/
"""

import sys
import os

from fabric.api import local, env, run, cd, lcd
from fabric.contrib import files, console
from fabric.colors import red, green, yellow
from fabric.context_managers import warn_only, quiet, prefix, hide
from contextlib import contextmanager as _contextmanager
from path import path

PROJECT_ROOT = path(__file__).abspath().realpath().dirname()
SITE_ROOT = PROJECT_ROOT / 'message_coding'
sys.path.append(SITE_ROOT)

_env_already_read = None


def _read_env():
    global _env_already_read

    if not _env_already_read:
        from message_coding import env_file

        _env_already_read = env_file.read(PROJECT_ROOT / '.env')

    return _env_already_read


_package_already_read = None


def _read_package():
    """Parse the package.json file"""
    global _package_already_read

    if not _package_already_read:
        import json

        with open(PROJECT_ROOT / 'package.json') as packfile:
            _package_already_read = json.load(packfile)
    return _package_already_read


def _get_settings():
    denv = _read_env()

    env.django_settings_module = denv.get('DJANGO_SETTINGS_MODULE', 'message_coding.settings.production')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.django_settings_module)

    from django.conf import settings

    return settings

def _symlink_supported():
    with quiet():
        if local('ln -s __linktest_target __linktest__source').succeeded:
            local('rm -f __linktest_source')
            return True
        return False

def dependencies():
    """Installs Python, NPM, and Bower packages"""

    _target_local()

    with lcd(PROJECT_ROOT):
        print green("Installing python requirements...")
        for req in env.pip_requirements:
            local('pip install -r %s | grep -vi "requirement already satisfied"' % req)

        if path('package.json').exists:
            print green("Installing node.js requirements...")
            if _symlink_supported():
                local('npm install')
            else:
                local('npm install --no-bin-link')

        if path('bower.json').exists:
            print green("Installing bower requirements...")
            local('bower install --config.interactive=false')
            local('bower prune --config.interactive=false')


def migrate():
    """Runs migrations"""

    _target_local()

    print green("Running migrations...")
    _manage_py('migrate')


def _manage_py(args):
    with lcd(SITE_ROOT):
        local('python manage.py %s' % args)


def production():
    """Builds static files for production"""

    _target_local()

    print green("Gathering and preprocessing static files...")
    _manage_py('collectstatic --noinput')
    _manage_py('compress')


def _target_local():
    package = _read_package()
    settings = _get_settings()

    env.machine_target = 'local'

    if env.django_settings_module == 'message_coding.settings.production':
        env.pip_requirements = ('requirements/production.txt',)
    else:
        env.pip_requirements = ('requirements/local.txt',)


def runserver():
    """Runs the Django development server"""

    _target_local()

    print green("Running the development webserver...")
    _manage_py('runserver 0.0.0.0:8000')


def load_test_data():
    _target_local()

    infile = PROJECT_ROOT / 'setup' / 'test_data.json'

    print green("Loading test data from %s" % infile)
    _manage_py("loaddata %s" % infile)


def make_test_data():
    """Updates the test_data.json file based on what is in the database"""
    _target_local()

    outfile = PROJECT_ROOT / 'setup' / 'test_data.json'
    apps = ' '.join(['base', 'coding', 'dataset', 'project', 'auth', '--exclude=auth.Permission'])

    print green("Saving test data from %s to %s" % (apps, outfile))
    _manage_py("dumpdata --indent=2 %s > %s" % (apps, outfile))

def reset_db():
    """Removes all of the tables"""
    _target_local()
    print red("WARNING! Deleting the database!")
    _manage_py("reset_db")


def interpolate_env(outpath=None):
    """Writes a .env file with variables interpolated from the current environment"""
    from django.template import Template, Context
    from django.conf import settings
    settings.configure()

    if outpath is None:
        outpath = PROJECT_ROOT / '.env'
    else:
        outpath = path(outpath)
    if outpath.exists():
        local('mv %s %s.bak' % (outpath, outpath))
        print "Backed up .env file to %s.bak" % outpath

    dot_env_path = PROJECT_ROOT / 'setup' / 'templates' / 'dot_env'

    with open(dot_env_path, 'rb') as infile:
        template = Template(infile.read())

        with open(outpath, 'wb') as outfile:
            outfile.write(template.render(Context(os.environ)))
