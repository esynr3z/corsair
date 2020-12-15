#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Run Corsair from command line with arguments.
"""

import sys
import os
import argparse
import corsair

__all__ = ['main']

writers_by_name = {
    'JSONWriter': corsair.JSONWriter(),
    'YAMLWriter': corsair.YAMLWriter()
}

writers_by_ext = {
    '.json': writers_by_name['JSONWriter'],
    '.yaml': writers_by_name['YAMLWriter'],
    '.yml': writers_by_name['YAMLWriter']
}

readers_by_name = {
    'JSONReader': corsair.JSONReader(),
    'YAMLReader': corsair.YAMLReader()
}

readers_by_ext = {
    '.json': readers_by_name['JSONReader'],
    '.yaml': readers_by_name['YAMLReader'],
    '.yml': readers_by_name['YAMLReader']
}


def arg_input(arg):
    """Validate input argument file[,ReaderClassName] and convert it to lambda function."""
    args = [x for x in arg.split(',')]
    if len(args) == 1:
        # use extension to choose agent
        _, csr_ext = os.path.splitext(args[0])
        csr_ext = csr_ext.lower()
        try:
            readers_by_ext[csr_ext]  # check if exists
            return lambda: readers_by_ext[csr_ext](args[0])
        except KeyError:  # unknown extension
            raise argparse.ArgumentError()
    else:
        # use provided name for the class
        try:
            readers_by_name[args[1]]  # check if exists
            return lambda: readers_by_name[args[1]](args[0])
        except KeyError:  # unknown class name
            raise argparse.ArgumentError()


def arg_output(arg):
    """Validate output argument file[,WriterClassName] and convert it to lambda function."""
    args = [x for x in arg.split(',')]
    if len(args) == 1:
        # use extension to choose agent
        _, csr_ext = os.path.splitext(args[0])
        csr_ext = csr_ext.lower()
        try:
            writers_by_ext[csr_ext]  # check if exists
            return lambda rmap: writers_by_ext[csr_ext](args[0], rmap)
        except KeyError:  # unknown extension
            raise argparse.ArgumentError()
    else:
        # use provided name for the class
        try:
            writers_by_name[args[1]]  # check if exists
            return lambda rmap: writers_by_name[args[1]](args[0], rmap)
        except KeyError:  # unknown class name
            raise argparse.ArgumentError()


class ArgumentParser(argparse.ArgumentParser):
    """Inherit ArgumentParser to override the behaviour of error method."""
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '\n%s: error: %s\n' % (self.prog, message))


def parse_arguments():
    """Parse and validate arguments."""
    parser = ArgumentParser(prog=corsair.__title__,
                            description=corsair.__description__)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s v' + corsair.__version__)
    parser.add_argument('-i', '--input',
                        type=arg_input,
                        metavar='file[,ReaderClassName]',
                        dest='reader',
                        help='read CSR map from file')
    parser.add_argument('-o', '--output',
                        type=arg_output,
                        metavar='file[,WriterClassName]',
                        nargs='+',
                        dest='writers',
                        help='write output to file(s)')
    parser.add_argument('-t', '--template',
                        type=arg_output,
                        metavar='file[,WriterClassName]',
                        dest='template_writer',
                        help='write CSR map template to file')
    parser.add_argument('--print-readers',
                        dest='need_print_readers',
                        action='store_true',
                        help='print names of all available readers')
    parser.add_argument('--print-writers',
                        dest='need_print_writers',
                        action='store_true',
                        help='print names of all available writers')

    # check if no arguments provided
    if len(sys.argv) == 1:
        parser.parse_args(['--help'])
        # argparse will raise SystemExit here

    # get arguments namespace
    args = parser.parse_args()

    # check for conflicts
    if not args.reader and args.writers:
        parser.error("Not able to use -o/--output without -i/--input argument!")

    return args


def main():
    """Program main."""
    # parse arguments
    args = parse_arguments()

    if args.need_print_readers:
        print('Readers available:')
        for name in readers_by_name.keys():
            print('  %s' % name)

    if args.need_print_writers:
        print('Writers available:')
        for name in writers_by_name.keys():
            print('  %s' % name)

    # create template if needed
    if args.template_writer:
        regs = [corsair.Register('spam', ' Register spam', 0),
                corsair.Register('eggs', ' Register eggs', 4)]
        regs[0].add_bfields([
            corsair.BitField('foo', 'Bit field foo', lsb=0, width=7, access='rw', initial=42),
            corsair.BitField('bar', 'Bit field bar', lsb=24, width=1, access='wo', modifiers=['self_clear'])
        ])
        regs[1].add_bfields(corsair.BitField('baz', 'Bit field baz', lsb=16, width=16, access='ro'))
        rmap = corsair.RegisterMap()
        rmap.add_regs(regs)
        args.template_writer(rmap)

    # parse CSR file
    if args.reader:
        rmap = args.reader()

    # create all output artifacts
    if args.writers:
        for writer in args.writers:
            writer(rmap)

    sys.exit(0)


if __name__ == '__main__':
    main()
