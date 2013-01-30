""" dump out all valid senders to use in Postfix filtering
"""
import logging

from karlserve.instance import set_current_instance
from karlserve.log import set_subsystem
from karl.utils import find_peopledirectory_catalog


log = logging.getLogger(__name__)


def config_parser(name, subparsers, **helpers):
    parser = subparsers.add_parser(
        name, help='dump out all valid senders to use in mail filtering')
    helpers['config_choose_instances'](parser)
    parser.set_defaults(func=main, parser=parser, subsystem='dump_senders',
                        only_one=True)


def main(args):
    for instance in args.instances:
        if not args.is_normal_mode(instance):
            log.info("Skipping %s: Running in maintenance mode." % instance)
            continue
        dump_senders(args, instance)


def dump_senders(args, instance):
    root, closer = args.get_root(instance)
    set_current_instance(instance)
    set_subsystem('dump_senders')

    pc = find_peopledirectory_catalog(root)

    for email in pc['email']._fwd_index.keys():
        if ',' in email:
            for e in email.split(','):
                if not e.isspace() and len(e) != 0:
                    print e.strip() + " permit_auth_destination"
        else:
            if not email.isspace() and len(email) != 0:
                print email.strip() + " permit_auth_destination"
