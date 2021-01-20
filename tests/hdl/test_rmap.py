#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for regmap module
"""

import sys
sys.path.append('../..')
import pytest
from sim import Simulator, CliArgs, path_join, parent_dir
import corsair


TEST_DIR = parent_dir(__file__)


def gen_rtl(tmpdir, bridge):
    config = corsair.Configuration()
    config['version'].value = '0.42'
    config['data_width'].value = 32
    config['address_width'].value = 12
    config['register_reset'].value = 'sync_pos'
    config['regmap']['read_filler'].value = 0xdeadc0de
    config['lb_bridge']['type'].value = bridge
    rmap = corsair.RegisterMap(config)

    # CSR LENA
    csr_lena = corsair.Register('LENA', 'Length of some pulse A', 0x0)
    csr_lena.add_bfields(corsair.BitField('VAL', 'CSR value', width=32, access='rw'))
    rmap.add_regs(csr_lena)

    # CSR LENB
    csr_lenb = corsair.Register('LENB', 'Length of some pulse B', 0x4)
    csr_lenb.add_bfields(corsair.BitField('VAL', 'CSR value', lsb=8, width=16, initial=0xFFFF, access='rw'))
    rmap.add_regs(csr_lenb)

    # CSR CNT
    csr_cnt = corsair.Register('CNT', 'Counter for some events', 0x10)
    csr_cnt.access_strobes = True
    csr_cnt.write_lock = True
    csr_cnt.add_bfields([
        corsair.BitField('EVA', 'Some event A counter',
                         lsb=0, width=12, initial=0x000, access='rw', modifiers=['hwu']),
        corsair.BitField('EVB', 'Some event B counter',
                         lsb=16, width=12, initial=0x000, access='rw', modifiers=['hwu'])])
    rmap.add_regs(csr_cnt)

    # CSR CTL
    csr_ctl = corsair.Register('CTL', 'Control something', 0x20)
    csr_ctl.add_bfields([
        corsair.BitField('DONE', 'Something is done status',
                         lsb=3, width=1, access='rw', modifiers=['hwu', 'w1tc']),
        corsair.BitField('GEN', 'Generate something',
                         lsb=5, width=1, access='rw', modifiers=['hwu', 'w1ts']),
        corsair.BitField('MODE', 'Mode of something',
                         lsb=16, width=1, access='rw', modifiers=['hwu', 'w1tt'])])
    rmap.add_regs(csr_ctl)

    # CSR START
    csr_start = corsair.Register('START', 'Start some process', 0x30)
    csr_start.write_lock = True
    csr_start.add_bfields([
        corsair.BitField('EN', 'Start some process A',
                         lsb=0, width=1, access='wo', modifiers=['sc']),
        corsair.BitField('KEY', 'Secret key',
                         lsb=16, width=16, access='wo')])
    rmap.add_regs(csr_start)

    # CSR STATUS
    csr_status = corsair.Register('STATUS', 'Some flags and status information', 0x40)
    csr_status.add_bfields([
        corsair.BitField('DIR', 'Current direction flag',
                         lsb=4, width=1, access='ro'),
        corsair.BitField('ERR', 'Some error flag',
                         lsb=8, width=1, access='ro', modifiers=['hwu']),
        corsair.BitField('CAP', 'Some captured value',
                         lsb=16, width=12, access='ro', modifiers=['hwu', 'rtc'])])
    rmap.add_regs(csr_status)

    # CSR VERSION
    csr_version = corsair.Register('VERSION', 'IP version', 0x44)
    csr_version.add_bfields([
        corsair.BitField('MINOR', 'Minor version',
                         lsb=0, width=8, access='ro', initial=0x10, modifiers=['const']),
        corsair.BitField('MAJOR', 'Major version',
                         lsb=16, width=8, access='ro', initial=0x02, modifiers=['const'])])
    rmap.add_regs(csr_version)

    # CSR INTSTAT
    csr_intstat = corsair.Register('INTSTAT', 'Interrupt status', 0x50, complementary=True)
    csr_intstat.add_bfields([
        corsair.BitField('CH0', 'Channel 0 interrupt',
                         lsb=0, width=1, access='ro'),
        corsair.BitField('CH1', 'Channel 1 interrupt',
                         lsb=1, width=1, access='ro')])
    rmap.add_regs(csr_intstat)

    # CSR INTCLR
    csr_intclr = corsair.Register('INTCLR', 'Interrupt clear', 0x50, complementary=True)
    csr_intclr.add_bfields([
        corsair.BitField('CH0', 'Channel 0 interrupt clear',
                         lsb=0, width=1, access='wo', modifiers=['sc']),
        corsair.BitField('CH1', 'Channel 1 interrupt clear',
                         lsb=1, width=1, access='wo', modifiers=['sc'])])
    rmap.add_regs(csr_intclr)

    regmap_path = path_join(tmpdir, 'regs.v')
    corsair.HdlWriter()(regmap_path, rmap)

    bridge_path = path_join(tmpdir, '%s2lb.v' % bridge)
    corsair.LbBridgeWriter()(bridge_path, config)
    return (regmap_path, bridge_path, rmap.config)


@pytest.fixture()
def simtool():
    return 'modelsim'


@pytest.fixture(params=['apb'])
def bridge(request):
    return request.param


@pytest.fixture(params=['tb_rw', 'tb_wo', 'tb_ro', 'tb_compl'])
def tb(request):
    return request.param


def test(tmpdir, tb, bridge, simtool, defines=[], gui=False, pytest_run=True):
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
    dut_src, bridge_src, config = gen_rtl(tmpdir, bridge)
    sim.sources += [dut_src, bridge_src]
    sim.defines += [
        'DUT_DATA_W=%d' % config['data_width'].value,
        'DUT_ADDR_W=%d' % config['address_width'].value,
        'BRIDGE_%s' % bridge.upper()
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
    cli.args_parser.add_argument('--bridge', default='apb', metavar='<bridge>', dest='bridge',
                                 help="bridge <bridge> to LocalBus; default is 'apb'")
    args = cli.parse()
    try:
        globals()[args.test](tmpdir='work',
                             tb=args.tb,
                             bridge=args.bridge,
                             simtool=args.simtool,
                             gui=args.gui,
                             defines=args.defines,
                             pytest_run=False)
    except KeyError:
        print("There is no test with name '%s'!" % args.test)
