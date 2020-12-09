#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Run CorSaiR from command line with arguments.
"""

import sys
import os
import argparse
import corsair


def create_parser():
    """Create program argument parser."""
    # inherit ArgumentParser to override the behaviour of error method
    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help(sys.stderr)
            self.exit(2, '\n%s: error: %s\n' % (self.prog, message))

    parser = ArgumentParser(prog=corsair.__title__,
                            description=corsair.__description__)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s v' + corsair.__version__)
    parser.add_argument(dest='csr_path',
                        metavar='CSR_FILE',
                        help='read CSR map from CSR_FILE')
    parser.add_argument('--json',
                        dest='json_path',
                        metavar='FILE',
                        help='write CSR map to JSON FILE')
    parser.add_argument('--yaml',
                        dest='yaml_path',
                        metavar='FILE',
                        help='write CSR map to YAML FILE')
    parser.add_argument('--verilog',
                        dest='verilog_path',
                        metavar='FILE',
                        help='write CSR map to Verilog FILE')
    return parser


def main():
    """Program main."""
    # parse arguments
    parser = create_parser()
    if len(sys.argv) == 1:  # if no arguments
        parser.parse_args(['--help'])
        # argparse will raise SystemExit here
    else:
        args = parser.parse_args()

    # prepare list of writers to use
    writers = {}
    output_paths = {}
    if args.json_path:
        writers['json'] = corsair.JSONWriter()
        output_paths['json'] = args.json_path
    if args.yaml_path:
        writers['yaml'] = corsair.YAMLWriter()
        output_paths['yaml'] = args.yaml_path
    if args.verilog_path:
        writers['verilog'] = lambda **args: print("Sorry, Verilog writer is not implemented yet,"
                                                  "'--verilog' key will be ignored.")
        output_paths['verilog'] = args.verilog_path

    # parse CSR file
    _, csr_file_ext = os.path.splitext(args.csr_path)
    csr_file_ext = csr_file_ext.lower()
    if csr_file_ext == '.json':
        reader = corsair.JSONReader()
    elif csr_file_ext in ['.yaml', '.yml']:
        reader = corsair.YAMLReader()
    else:
        parser.error("CSR_FILE '%s' has unknown extension '%s'!" % (args.csr_path, csr_file_ext))
    rmap = reader(args.csr_path)

    # create all output artifacts
    for k in writers.keys():
        writers[k](path=output_paths[k], rmap=rmap)

    sys.exit(0)


if __name__ == '__main__':
    main()
