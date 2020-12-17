#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Run Corsair from command line with arguments.
"""

import sys
import os
import argparse
import corsair

__all__ = ['main']

writers = {
    'csr_map_json': corsair.JSONWriter(),
    'csr_map_yaml': corsair.YAMLWriter()
}

writers_default_ext = {
    '.json': 'csr_map_json',
    '.yaml': 'csr_map_yaml',
    '.yml': 'csr_map_yaml'
}

readers = {
    'csr_map_json': corsair.JSONReader(),
    'csr_map_yaml': corsair.YAMLReader()
}

readers_default_ext = {
    '.json': 'csr_map_json',
    '.yaml': 'csr_map_yaml',
    '.yml': 'csr_map_yaml'
}

template_writers = {
    'csr_map_json': corsair.JSONWriter(),
    'csr_map_yaml': corsair.YAMLWriter()
}


def arg_input(arg):
    """Validate input argument file[,type] and return dictionary with path and reader object."""
    args = [x for x in arg.split(',')]
    if len(args) == 1:
        # use extension to choose reader
        _, csr_ext = os.path.splitext(args[0])
        csr_ext = csr_ext.lower()
        try:
            return {'path': args[0], 'obj': readers[readers_default_ext[csr_ext]]}
        except KeyError:  # unknown extension
            print('unknown extension')
            raise argparse.ArgumentError()
    else:
        # use provided name for the input type
        try:
            return {'path': args[0], 'obj': readers[args[1]]}
        except KeyError:  # unknown input type
            raise argparse.ArgumentError()


def arg_output(arg):
    """Validate output argument file[,type] and return dictionary with path and writer object."""
    args = [x for x in arg.split(',')]
    if len(args) == 1:
        # use extension to choose writer
        _, csr_ext = os.path.splitext(args[0])
        csr_ext = csr_ext.lower()
        try:
            return {'path': args[0], 'obj': writers[writers_default_ext[csr_ext]]}
        except KeyError:  # unknown extension
            raise argparse.ArgumentError()
    else:
        # use provided name for the output type
        try:
            return {'path': args[0], 'obj': writers[args[1]]}
        except KeyError:  # unknown output type
            raise argparse.ArgumentError()


class ArgumentParser(argparse.ArgumentParser):
    """Inherit ArgumentParser to override the behaviour of error method."""
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '\n%s: error: %s\n' % (self.prog, message))


def parse_arguments():
    """Parse and validate arguments."""

    description = corsair.__description__
    description += """


Multiple -o/--output arguments can be specified:
    corsair -i csr.json -o regmap.v -o regmap.md
"""
    description += "\nAvailable input types for -i/--input argument:\n"
    for name in readers.keys():
        description += "  %s - %s\n" % (name, readers[name].description)
    description += "If no input type is specified explicitly, it will be chosen based on the file extension:\n"
    for ext in readers_default_ext.keys():
        description += "  %s - %s\n" % (ext, readers_default_ext[ext])

    description += "\nAvailable output types for -o/--output argument:\n"
    for name in writers.keys():
        description += "  %s - %s\n" % (name, writers[name].description)
    description += "If no output type is specified explicitly, it will be chosen based on the file extension:\n"
    for ext in writers_default_ext.keys():
        description += "  %s - %s\n" % (ext, writers_default_ext[ext])

    description += "\nAvailable output types for -t/--template argument:\n"
    for name in template_writers.keys():
        description += "  %s\n" % name
    description += "If no output type is specified explicitly, "
    description += "it will be chosen based on the file extension as for -o/--output\n"

    parser = ArgumentParser(prog=corsair.__title__,
                            description=description,
                            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s v' + corsair.__version__)
    parser.add_argument('-i', '--input',
                        type=arg_input,
                        metavar='file[,type]',
                        dest='reader',
                        help='read CSR map from file; input type can be specified explicitly')
    parser.add_argument('-o', '--output',
                        type=arg_output,
                        metavar='file[,type]',
                        action='append',
                        dest='writers',
                        help='write output to file; output type can be specified explicitly')
    parser.add_argument('-t', '--template',
                        type=arg_output,
                        metavar='file[,type]',
                        dest='template_writer',
                        help='write template to file; template type can be specified explicitly')

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

    # create template if needed
    if args.template_writer:
        # prepare rmap
        regs = [corsair.Register('spam', ' Register spam', 0),
                corsair.Register('eggs', ' Register eggs', 4)]
        regs[0].add_bfields([
            corsair.BitField('foo', 'Bit field foo', lsb=0, width=7, access='rw', initial=42),
            corsair.BitField('bar', 'Bit field bar', lsb=24, width=1, access='wo', modifiers=['self_clear'])
        ])
        regs[1].add_bfields(corsair.BitField('baz', 'Bit field baz', lsb=16, width=16, access='ro'))
        rmap = corsair.RegisterMap()
        rmap.add_regs(regs)
        # write template
        output_path = args.template_writer['path']
        template_writer = args.template_writer['obj']
        template_writer(path=output_path, rmap=rmap)

    # parse CSR file
    if args.reader:
        input_path = args.reader['path']
        reader = args.reader['obj']
        rmap = reader(input_path)

    # create all output artifacts
    if args.writers:
        for arg_writer in args.writers:
            output_path = arg_writer['path']
            writer = arg_writer['obj']
            writer(path=output_path, rmap=rmap)

    sys.exit(0)


if __name__ == '__main__':
    main()
