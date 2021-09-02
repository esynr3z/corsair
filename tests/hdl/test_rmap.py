#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for regmap module
"""

import sys
sys.path.insert(0, '../..')
import pytest
from sim import Simulator, CliArgs, path_join, parent_dir
from corsair import config, generators, RegisterMap, Register, BitField


TEST_DIR = parent_dir(__file__)


def gen_rtl(tmpdir, interface, reset, hdl):
    # global configuration
    globcfg = config.default_globcfg()
    globcfg['data_width'] = 32
    globcfg['address_width'] = 12
    globcfg['register_reset'] = reset
    config.set_globcfg(globcfg)

    # register map
    rmap = RegisterMap()
    rmap.add_registers(Register('REGRW', 'register rw', 0x0).add_bitfields([
        BitField("BFO", "bitfield o", width=3, lsb=1, access='rw', reset=5, hardware='o'),
        BitField("BFIOE", "bitfield ioe", width=4, lsb=4, access='rw', hardware='ioe'),
        BitField("BFIOEA", "bitfield ioa", width=2, lsb=8, access='rw', hardware='ioea'),
        BitField("BFOL", "bitfield ol", width=8, lsb=10, access='rw', hardware='ol'),
        BitField("BFOS", "bitfield os", width=1, lsb=18, access='rw', hardware='os'),
        BitField("BFOC", "bitfield oc", width=1, lsb=23, access='rw', hardware='oc'),
        BitField("BFN", "bitfield n", width=8, lsb=24, access='rw', hardware='n'),
    ]))
    rmap.add_registers(Register('REGRWQ', 'register rw queue', 0x4).add_bitfields([
        BitField("BFIOQ", "bitfield ioq", width=12, lsb=0, access='rw', hardware='q'),
    ]))
    rmap.add_registers(Register('REGRW1X', 'register rw1x', 0x8).add_bitfields([
        BitField("BFC", "bitfield rw1c s", width=1, lsb=1, access='rw1c', hardware='s'),
        BitField("BFS", "bitfield rw1s c", width=1, lsb=4, access='rw1s', reset=1, hardware='c'),
    ]))
    rmap.add_registers(Register('REGRO', 'register ro', 0x10).add_bitfields([
        BitField("BFI", "bitfield ro i", width=8, lsb=0, access='ro', hardware='i'),
        BitField("BFF", "bitfield ro f", width=4, lsb=8, access='ro', hardware='f', reset=13),
        BitField("BFIE", "bitfield ro ie", width=4, lsb=12, access='ro', hardware='ie'),
    ]))
    rmap.add_registers(Register('REGROC', 'register ro', 0x14).add_bitfields([
        BitField("BFIE", "bitfield roc ie", width=16, lsb=0, access='roc', hardware='ie'),
    ]))
    rmap.add_registers(Register('REGROQ', 'register ro queue', 0x20).add_bitfields([
        BitField("BFIQ", "bitfield ro iq", width=24, lsb=0, access='ro', hardware='q'),
    ]))
    rmap.add_registers(Register('REGROLX', 'register roll / rolh', 0x24).add_bitfields([
        BitField("BFLL", "bitfield roll i", width=1, lsb=0, access='roll', reset=1, hardware='i'),
        BitField("BFLH", "bitfield rolh i", width=1, lsb=16, access='rolh', hardware='i'),
        BitField("BFLLE", "bitfield roll ie", width=1, lsb=23, access='roll', reset=1, hardware='ie'),
        BitField("BFLHE", "bitfield rolh ie", width=1, lsb=28, access='rolh', hardware='ie'),
    ]))
    rmap.add_registers(Register('REGWO', 'register wo / wosc', 0x28).add_bitfields([
        BitField("BFWO", "bitfield wo o", width=4, lsb=8, access='wo', hardware='o'),
        BitField("BFSC", "bitfield wosc o", width=1, lsb=16, access='wosc', hardware='o'),
    ]))
    rmap.add_registers(Register('REGWOQ', 'register wo queue', 0x30).add_bitfields([
        BitField("BFOQ", "bitfield wo oq", width=24, lsb=0, access='wo', hardware='q'),
    ]))

    if hdl == 'vhdl':
        regmap_path = path_join(tmpdir, 'regs.vhd')
        generators.Vhdl(rmap, regmap_path, read_filler=0xdeadc0de, interface=interface).generate()
    else:
        regmap_path = path_join(tmpdir, 'regs.v')
        generators.Verilog(rmap, regmap_path, read_filler=0xdeadc0de, interface=interface).generate()

    header_path = path_join(tmpdir, 'regs.vh')
    generators.VerilogHeader(rmap, header_path).generate()

    package_path = path_join(tmpdir, 'regs_pkg.sv')
    generators.SystemVerilogPackage(rmap, package_path).generate()

    return (package_path, regmap_path)


@pytest.fixture()
def simtool():
    return 'modelsim'


@pytest.fixture(params=['apb', 'axil', 'amm'])
def interface(request):
    return request.param


@pytest.fixture(params=['verilog', 'vhdl'])
def hdl(request):
    return request.param


@pytest.fixture(params=['sync_pos', 'sync_neg', 'async_pos', 'async_neg'])
def reset(request):
    return request.param


@pytest.fixture(params=['tb_rw', 'tb_wo', 'tb_ro'])
def tb(request):
    return request.param


def test(tmpdir, tb, interface, reset, hdl, simtool, defines=[], gui=False, pytest_run=True):
    # create sim
    tb_dir = path_join(TEST_DIR, 'test_rmap')
    beh_dir = path_join(TEST_DIR, 'beh')
    sim = Simulator(name=simtool, gui=gui, cwd=tmpdir)
    sim.incdirs += [tmpdir, tb_dir, beh_dir]
    sim.sources += [path_join(tb_dir, '%s.sv' % tb)]
    sim.sources += beh_dir.glob('*.sv')
    sim.defines += defines
    sim.top = tb
    sim.setup()
    # prepare test
    src = gen_rtl(tmpdir, interface, reset, hdl)
    sim.sources = list(src) + sim.sources
    sim.defines += [
        'INTERFACE_%s' % interface.upper(),
        'RESET_ACTIVE=%d' % ('pos' in reset),
    ]
    # run sim
    sim.run()
    if pytest_run:
        assert sim.is_passed


if __name__ == '__main__':
    # run script with key -h to see help
    cli = CliArgs(default_test='test')
    cli.args_parser.add_argument('--tb', default='tb_rw', metavar='<tb>', dest='tb',
                                 help="run testbench named <tb>; default is 'tb_rw'")
    cli.args_parser.add_argument('--interface', default='apb', metavar='<interface>', dest='interface',
                                 help="interface <interface> to register map; default is 'apb'")
    cli.args_parser.add_argument('--reset', default='sync_pos', metavar='<reset>', dest='reset',
                                 help="reset <reset> for interface registers; default is 'sync_pos'")
    cli.args_parser.add_argument('--hdl', default='verilog', metavar='<hdl>', dest='hdl',
                                 help="choosen HDL; default is 'verilog'")
    args = cli.parse()
    try:
        globals()[args.test](tmpdir='work',
                             tb=args.tb,
                             interface=args.interface,
                             reset=args.reset,
                             hdl=args.hdl,
                             simtool=args.simtool,
                             gui=args.gui,
                             defines=args.defines,
                             pytest_run=False)
    except KeyError:
        print("There is no test with name '%s'!" % args.test)
