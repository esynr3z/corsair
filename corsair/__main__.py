#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Run Corsair from command line with arguments.
"""

import sys
import os
import argparse
from pathlib import Path
import corsair
from . import utils
from contextlib import contextmanager
import importlib.util

__all__ = ['main']


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


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
    parser.add_argument(metavar='WORKDIR',
                        nargs='?',
                        dest='workdir_path',
                        default=os.getcwd(),
                        help='working directory (default is the current directory)')
    parser.add_argument('-r',
                        metavar='REGMAP',
                        dest='regmap_path',
                        help='read register map from file')
    parser.add_argument('-c',
                        metavar='CONFIG',
                        dest='config_path',
                        help='read configuration from file')
    template_choices = ['json', 'yaml', 'txt']
    parser.add_argument('-t',
                        metavar='FORMAT',
                        choices=template_choices,
                        dest='template_format',
                        help='create templates (choose from %s)' % ', '.join(template_choices))
    return parser.parse_args()


def generate_templates(format):
    print("... templates format: '%s'" % format)
    # global configuration
    globcfg = corsair.config.default_globcfg()
    globcfg['data_width'] = 32
    globcfg['address_width'] = 16
    globcfg['register_reset'] = 'sync_pos'
    corsair.config.set_globcfg(globcfg)

    # targets
    targets = {}
    targets.update(corsair.generators.Verilog(path="hw/regs.v").make_target('v_module'))
    targets.update(corsair.generators.Vhdl(path="hw/regs.vhd").make_target('vhdl_module'))
    targets.update(corsair.generators.VerilogHeader(path="hw/regs.vh").make_target('v_header'))
    targets.update(corsair.generators.SystemVerilogPackage(path="hw/regs_pkg.sv").make_target('sv_pkg'))
    targets.update(corsair.generators.Python(path="sw/regs.py").make_target('py'))
    targets.update(corsair.generators.CHeader(path="sw/regs.h").make_target('c_header'))
    targets.update(corsair.generators.Markdown(path="doc/regs.md", image_dir="md_img").make_target('md_doc'))
    targets.update(corsair.generators.Asciidoc(path="doc/regs.adoc", image_dir="adoc_img").make_target('asciidoc_doc'))

    # create templates
    if format == 'txt':
        rmap = corsair.utils.create_template_simple()
    else:
        rmap = corsair.utils.create_template()
    # register map template
    if format == 'json':
        gen = corsair.generators.Json(rmap)
        regmap_path = 'regs.json'
    elif format == 'yaml':
        gen = corsair.generators.Yaml(rmap)
        regmap_path = 'regs.yaml'
    elif format == 'txt':
        gen = corsair.generators.Txt(rmap)
        regmap_path = 'regs.txt'
    print("... generate register map file '%s'" % regmap_path)
    gen.generate()
    # configuration file template
    config_path = 'csrconfig'
    globcfg['regmap_path'] = regmap_path
    print("... generate configuration file '%s'" % config_path)
    corsair.config.write_csrconfig(config_path, globcfg, targets)


def die(msg):
    print("Error: %s" % msg)
    exit(1)


def finish():
    print('Success!')
    exit(0)


def app(args):
    print("... set working directory '%s'" % args.workdir_path)

    # check if teplates are needed
    if args.template_format:
        generate_templates(args.template_format)
        finish()

    # check if configuration file path was provided
    if args.config_path:
        config_path = Path(args.config_path)
    else:
        config_path = Path('csrconfig')
    # check it existance
    if not config_path.is_file():
        die("Can't find configuration file '%s'!" % config_path)
    # try to read it
    print("... read configuration file '%s'" % config_path)
    globcfg, targets = corsair.config.read_csrconfig(config_path)

    # check if regiter map file path was provided
    if args.regmap_path:
        regmap_path = Path(args.regmap_path)
        globcfg['regmap_path'] = regmap_path
    elif 'regmap_path' in globcfg.keys():
        regmap_path = Path(globcfg['regmap_path'])
    else:
        regmap_path = None
        print("Warning: No register map file was specified!")
    corsair.config.set_globcfg(globcfg)

    if regmap_path:
        # check it existance
        if not regmap_path.is_file():
            die("Can't find register map file '%s'!" % regmap_path)
        # try to read it
        print("... read register map file '%s'" % regmap_path)
        rmap = corsair.RegisterMap()
        rmap.read_file(regmap_path)
        print("... validate register map")
        rmap.validate()
    else:
        rmap = None

    # make targets
    if not targets:
        die("No targets were specified! Nothing to do!")
    for t in targets:
        print("... make '%s': " % t, end='')
        if 'generator' not in targets[t].keys():
            die("No generator was specified for the target!")

        if '.py::' in targets[t]['generator']:
            custom_module_path, custom_generator_name = targets[t]['generator'].split('::')
            custom_module_name = utils.get_file_name(custom_module_path)
            spec = importlib.util.spec_from_file_location(custom_module_name, custom_module_path)
            custom_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(custom_module)
            try:
                gen_obj = getattr(custom_module, custom_generator_name)
                gen_name = custom_generator_name
            except AttributeError:
                die("Generator '%s' from module '%s' does not exist!" % (custom_generator_name, custom_module_path))
        else:
            gen_name = targets[t]['generator']
            try:
                gen_obj = getattr(corsair.generators, gen_name)
            except AttributeError:
                die("Generator '%s' does not exist!" % gen_name)

        gen_args = targets[t]
        print("%s -> '%s': " % (gen_name, gen_args['path']))
        gen_obj(rmap, **gen_args).generate()


def main():
    """Program main"""
    # parse arguments
    args = parse_arguments()

    # do all the things inside working directory
    args.workdir_path = str(Path(args.workdir_path).absolute())
    with cwd(args.workdir_path):
        app(args)
    finish()


if __name__ == '__main__':
    main()
