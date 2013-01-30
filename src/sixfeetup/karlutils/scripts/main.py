from __future__ import with_statement

import argparse
import codecs
import logging
import pkg_resources
import sys

from paste.deploy import loadapp

from karlserve.instance import get_instances
from karlserve.scripts.main import config_choose_instances
from karlserve.scripts.main import config_daemon_mode
from karlserve.scripts.main import get_default_config
from karlserve.scripts.main import instance_factory
from karlserve.scripts.main import instance_root_factory
from karlserve.scripts.main import debug
from karlserve.scripts.main import only_one
from karlserve.scripts.main import daemon
from karlserve.scripts.main import is_normal_mode
from karlserve.scripts.main import settings_factory

_marker = object

log = logging.getLogger(__name__)


def main(argv=sys.argv, out=None):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s')

    # ZEO is a bit too chatty, if you ask me.
    zeo_logger = logging.getLogger('ZEO')
    zeo_logger.setLevel(logging.WARN)

    if out is None:
        out = codecs.getwriter('UTF-8')(sys.stdout)

    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--config', metavar='FILE', default=None,
                        help='Path to configuration ini file.')
    parser.add_argument('--pdb', action='store_true', default=False,
                        help='Drop into the debugger if there is an uncaught '
                        'exception.')

    subparsers = parser.add_subparsers(
        title='command', help='Available commands.')
    eps = [ep for ep in pkg_resources.iter_entry_points('iwlearn.scripts')]
    eps.sort(key=lambda ep: ep.name)
    ep_names = set()
    for ep in eps:
        if ep.name in ep_names:
            raise RuntimeError('script defined more than once: %s' % ep.name)
        try:
            script = ep.load()
            ep_names.add(ep.name)
            script(ep.name, subparsers, **helpers)
        except ImportError:
            pass

    args = parser.parse_args(argv[1:])
    if args.config is None:
        args.config = get_default_config()

    app = loadapp('config:%s' % args.config, 'karlserve')
    if hasattr(args, 'instance'):
        if not args.instance:
            args.instances = sorted(get_instances(
                app.registry.settings).get_names())
        else:
            args.instances = sorted(args.instance)
        del args.instance

    args.app = app
    args.get_instance = instance_factory(args, app)
    args.get_root = instance_root_factory(args, app)
    args.get_setting = settings_factory(args, app)
    args.is_normal_mode = is_normal_mode(args)
    args.out = out
    try:
        func = log_errors(args.func)
        if getattr(args, 'daemon', False):
            func = daemon(func, args)
        if getattr(args, 'only_one', False):
            func = only_one(func, args)
        if args.pdb:
            func = debug(func)
        func(args)
    finally:
        instances = app.registry.settings.get('instances')
        if instances is not None:
            instances.close()


def log_errors(func):
    def wrapper(args):
        try:
            return func(args)
        except:
            logging.getLogger(func.__module__).error(
                "Error in script.", exc_info=True)

    return wrapper

helpers = {
    'config_choose_instances': config_choose_instances,
    'config_daemon_mode': config_daemon_mode,
}
