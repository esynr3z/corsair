#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for axil2lb module
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


def gen_axil2lb(tmpdir):
    config = corsair.Configuration()
    config['lb_bridge']['type'].value = 'axil'

    axil2lb_path = str(Path(tmpdir) / 'axil2lb.v')
    corsair.LbBridgeWriter()(axil2lb_path, config)
    return (axil2lb_path, config)


def test_common(tmpdir, simtool, gui=False, validate=True):
    tb_dir = Path(__file__).parent / Path(__file__).stem
    tb_dir_path = str(tb_dir)
    tb_name = 'tb_common'
    tb_filename = tb_name + '.sv'
    tb_path = str(tb_dir / tb_filename)
    dut_path, dut_config = gen_axil2lb(tmpdir)

    sim = Simulator(simtool)
    sim.incdirs += [tb_dir_path]
    sim.sources += [tb_path, dut_path]
    sim.defines += [
        'DUT_DATA_W=%d' % dut_config['data_width'].value,
        'DUT_ADDR_W=%d' % dut_config['address_width'].value
    ]
    sim.top = tb_name
    retval = sim.run(gui)
    if validate:
        assert '!@# TEST PASSED #@!' in sim.stdout


if __name__ == '__main__':
    # run script with key -h to see help
    tmpdir = tempfile.gettempdir()
    tb_dict = {
        'tb_common': lambda tool, gui: test_common(tmpdir, simtool=tool, gui=gui, validate=False),
    }
    sim = Simulation(
        default_tb='tb_common',
        default_tool='icarus',
        default_gui=True,
        tb_dict=tb_dict)
    sim.run()
