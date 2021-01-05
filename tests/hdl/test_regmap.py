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


def gen_regmap(tmpdir):
    config = corsair.Configuration()
    config['version'].value = '0.42'
    config['data_width'].value = 32
    config['address_width'].value = 12
    config['regmap']['read_filler'].value = 0xdeadc0de
    rmap = corsair.RegisterMap(config)

    # CSR LEN
    csr_len = corsair.Register('LEN', 'Length of pulse', 0x0)
    csr_len.add_bfields(corsair.BitField('VAL', 'CSR value', width=32, access='rw'))
    rmap.add_regs(csr_len)

    # CSR CNT
    csr_cnt = corsair.Register('CNT', 'Counter', 0x4)
    csr_cnt.add_bfields(corsair.BitField('VAL', 'CSR value', lsb=8, width=16, access='rw'))
    rmap.add_regs(csr_cnt)

    regmap_path = str(Path(tmpdir) / 'regs.v')
    corsair.HdlWriter()(regmap_path, rmap)
    return (regmap_path, rmap)


def test_common(tmpdir, simtool, gui=False, validate=True):
    pass
    # tb_dir = Path(__file__).parent / Path(__file__).stem
    # tb_dir_path = str(tb_dir)
    # tb_name = 'tb_common'
    # tb_filename = tb_name + '.sv'
    # tb_path = str(tb_dir / tb_filename)
    # dut_path, dut_config = gen_apb2lb(tmpdir)
    # sim = Simulator(simtool)
    # sim.incdirs += [tb_dir_path]
    # sim.sources += [tb_path, dut_path]
    # sim.defines += [
    #     'DUT_DATA_W=%d' % dut_config['data_width'].value,
    #     'DUT_ADDR_W=%d' % dut_config['address_width'].value
    # ]
    # sim.top = tb_name
    # retval = sim.run(gui)
    # if validate:
    #     assert '!@# TEST PASSED #@!' in sim.stdout


if __name__ == '__main__':
    # run script with key -h to see help
    tmpdir = tempfile.gettempdir()
    gen_regmap(tmpdir)
    # tb_dict = {
    #     'tb_common': lambda tool, gui: test_common(tmpdir, simtool=tool, gui=gui, validate=False),
    # }
    # sim = Simulation(
    #     default_tb='tb_common',
    #     default_tool='icarus',
    #     default_gui=True,
    #     tb_dict=tb_dict)
    # sim.run()
