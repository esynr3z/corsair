#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Run Corsair from command line with arguments.
"""

import sys
import os
import argparse
import corsair
from . import utils

__all__ = ['main']


class ArgumentParser(argparse.ArgumentParser):
    """Inherit ArgumentParser to override the behaviour of error method."""
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '\n%s: error: %s\n' % (self.prog, message))


def check_json_yaml(file):
    if get_file_ext(file) not in ['.json', '.yaml', '.yml'] <= 0:
        raise argparse.ArgumentTypeError("%s has wrong extension!" % file)
    return file


def parse_arguments():
    """Parse and validate arguments."""

    parser = ArgumentParser(prog=corsair.__title__,
                            description=corsair.__description__)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s v' + corsair.__version__)
    parser.add_argument('-r', '--reg-map',
                        type=check_json_yaml,
                        metavar='file',
                        dest='reg_map',
                        help='read register map from file')
    parser.add_argument('-c', '--config',
                        type=check_json_yaml,
                        metavar='file',
                        dest='config',
                        help='read configuration from file')
    parser.add_argument('-t', '--template',
                        dest='template',
                        const='json',
                        default=None,
                        action='store',
                        nargs='?',
                        type=str,
                        choices=['json', 'yaml'],
                        help='create register map template file in selected format (default: %(const)s)'),
    parser.add_argument('--hdl',
                        dest='hdl',
                        const='verilog',
                        default=None,
                        action='store',
                        nargs='?',
                        type=str,
                        choices=['verilog', 'vhdl'],
                        help='create register map HDL files in selected language (default: %(const)s)')
    parser.add_argument('--doc',
                        dest='doc',
                        const='markdown',
                        default=None,
                        action='store',
                        nargs='?',
                        type=str,
                        choices=['markdown', 'pdf'],
                        help='create docs for register map in selected format (default: %(const)s)')

    # check if no arguments provided
    if len(sys.argv) == 1:
        parser.parse_args(['--help'])
        # argparse will raise SystemExit here

    # get arguments namespace
    args = parser.parse_args()
    exit(0)
    return args


def main():
    """Program main."""
    # parse arguments
    args = parse_arguments()

    # create template if needed
    if args.template:
        pass

    # parse configuration file
    if args.config:
        pass

    # parse register map file
    if args.reg_map:
        pass

    # create hdl
    if args.hdl:
        pass

    # create docs
    if args.docs:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
