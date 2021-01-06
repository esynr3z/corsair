#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for regmap module
"""

import sys
sys.path.append('../..')
import tempfile
import pytest
from pathlib import Path
from sim import Simulator, Simulation
import corsair


@pytest.fixture()
def simtool():
    return 'icarus'


def gen_rtl(tmpdir):
    config = corsair.Configuration()
    config['version'].value = '0.42'
    config['data_width'].value = 32
    config['address_width'].value = 12
    config['register_reset'].value = 'sync_pos'
    config['regmap']['read_filler'].value = 0xdeadc0de
    config['lb_bridge']['type'].value = 'apb'
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
    csr_cnt.add_bfields([
        corsair.BitField('EVA', 'Some event A counter',
                         lsb=0, width=12, initial=0x000, access='rw', modifiers=['external_update']),
        corsair.BitField('EVB', 'Some event B counter',
                         lsb=16, width=12, initial=0x000, access='rw', modifiers=['external_update'])])
    rmap.add_regs(csr_cnt)

    # CSR CTL
    csr_ctl = corsair.Register('CTL', 'Control something', 0x20)
    csr_ctl.add_bfields([
        corsair.BitField('DONE', 'Something is done status',
                         lsb=3, width=1, access='rw', modifiers=['external_update', 'write1_to_clear']),
        corsair.BitField('GEN', 'Generate something',
                         lsb=5, width=1, access='rw', modifiers=['external_update', 'write1_to_set']),
        corsair.BitField('MODE', 'Mode of something',
                         lsb=16, width=1, access='rw', modifiers=['external_update', 'write1_to_toggle'])])
    rmap.add_regs(csr_ctl)

    # CSR START
    csr_start = corsair.Register('START', 'Start some process', 0x30)
    csr_start.add_bfields([
        corsair.BitField('EN', 'Start some process A',
                         lsb=0, width=1, access='wo', modifiers=['self_clear']),
        corsair.BitField('KEY', 'Secret key',
                         lsb=16, width=16, access='wo')])
    rmap.add_regs(csr_start)

    # CSR STATUS
    csr_status = corsair.Register('STATUS', 'Some flags and status information', 0x40)
    csr_status.add_bfields([
        corsair.BitField('DIR', 'Current direction flag',
                         lsb=4, width=1, access='ro'),
        corsair.BitField('ERR', 'Some error flag',
                         lsb=8, width=1, access='ro', modifiers=['external_update']),
        corsair.BitField('CAP', 'Some captured value',
                         lsb=16, width=12, access='ro', modifiers=['external_update', 'read_to_clear'])])
    rmap.add_regs(csr_status)

    # CSR VERSION
    csr_version = corsair.Register('VERSION', 'IP version', 0x44)
    csr_version.add_bfields([
        corsair.BitField('MINOR', 'Minor version',
                         lsb=0, width=8, access='ro', initial=0x10, modifiers=['read_const']),
        corsair.BitField('MAJOR', 'Major version',
                         lsb=16, width=8, access='ro', initial=0x02, modifiers=['read_const'])])
    rmap.add_regs(csr_version)

    regmap_path = str(Path(tmpdir) / 'regs.v')
    corsair.HdlWriter()(regmap_path, rmap)

    apb2lb_path = str(Path(tmpdir) / 'apb2lb.v')
    corsair.LbBridgeWriter()(apb2lb_path, config)
    return (regmap_path, apb2lb_path, rmap.config)


def _test(tb_name, tmpdir, simtool, gui=False, validate=True):
    tb_dir = Path(__file__).parent / Path(__file__).stem
    tb_dir_path = str(tb_dir.resolve())
    tb_filename = tb_name + '.sv'
    tb_path = str(tb_dir / tb_filename)
    dut_path, bridge_path, config = gen_rtl(tmpdir)
    sim = Simulator(simtool)
    sim.incdirs += [tb_dir_path]
    sim.sources += [tb_path, dut_path, bridge_path]
    sim.defines += [
        'DUT_DATA_W=%d' % config['data_width'].value,
        'DUT_ADDR_W=%d' % config['address_width'].value
    ]
    sim.top = tb_name
    retval = sim.run(gui)
    if validate:
        assert '!@# TEST PASSED #@!' in sim.stdout


def test_rw(tmpdir, simtool, gui=False, validate=True):
    tb_name = 'tb_rw'
    _test(tb_name, tmpdir=tmpdir, simtool=simtool, gui=gui, validate=validate)


def test_wo(tmpdir, simtool, gui=False, validate=True):
    tb_name = 'tb_wo'
    _test(tb_name, tmpdir=tmpdir, simtool=simtool, gui=gui, validate=validate)


def test_ro(tmpdir, simtool, gui=False, validate=True):
    tb_name = 'tb_ro'
    _test(tb_name, tmpdir=tmpdir, simtool=simtool, gui=gui, validate=validate)


if __name__ == '__main__':
    # run script with key -h to see help
    tmpdir = tempfile.gettempdir()
    tb_dict = {
        'tb_rw': lambda tool, gui: test_rw(tmpdir, simtool=tool, gui=gui, validate=False),
        'tb_wo': lambda tool, gui: test_wo(tmpdir, simtool=tool, gui=gui, validate=False),
        'tb_ro': lambda tool, gui: test_ro(tmpdir, simtool=tool, gui=gui, validate=False),
    }
    sim = Simulation(
        default_tb='tb_rw',
        default_tool='icarus',
        default_gui=True,
        tb_dict=tb_dict)
    sim.run()
