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

    # CSR LEN
    csr_len = corsair.Register('LEN', 'Length of pulse', 0x0)
    csr_len.add_bfields(corsair.BitField('VAL', 'CSR value', width=32, access='rw'))
    rmap.add_regs(csr_len)

    # CSR CNT
    csr_cnt = corsair.Register('CNT', 'Counter', 0x4)
    csr_cnt.add_bfields(corsair.BitField('VAL', 'CSR value', lsb=8, width=16, initial=0xFFFF, access='rw'))
    rmap.add_regs(csr_cnt)

    regmap_path = str(Path(tmpdir) / 'regs.v')
    corsair.HdlWriter()(regmap_path, rmap)

    apb2lb_path = str(Path(tmpdir) / 'apb2lb.v')
    corsair.LbBridgeWriter()(apb2lb_path, config)
    return (regmap_path, apb2lb_path, rmap.config)


def test_rw(tmpdir, simtool, gui=False, validate=True):
    tb_dir = Path(__file__).parent / Path(__file__).stem
    tb_dir_path = str(tb_dir)
    tb_name = 'tb_rw'
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


if __name__ == '__main__':
    # run script with key -h to see help
    tmpdir = tempfile.gettempdir()
    tb_dict = {
        'tb_rw': lambda tool, gui: test_rw(tmpdir, simtool=tool, gui=gui, validate=False),
    }
    sim = Simulation(
        default_tb='tb_rw',
        default_tool='icarus',
        default_gui=True,
        tb_dict=tb_dict)
    sim.run()
