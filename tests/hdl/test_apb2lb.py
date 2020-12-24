#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for apb2lb module
"""

import sys
sys.path.append('../..')
import tempfile
import pytest
from pathlib import Path
from sim import Simulator
import corsair


@pytest.fixture()
def simtool():
    return 'icarus'


def gen_apb2lb(tmpdir):
    config = corsair.Configuration()
    config['lb_bridge']['type'].value = 'apb'

    apb2lb_path = str(Path(tmpdir) / 'apb2lb.v')
    corsair.LbBridgeWriter()(apb2lb_path, config)
    return apb2lb_path


def test_common(tmpdir, simtool, gui=False, validate=True):
    tb_dir = Path(__file__).parent / Path(__file__).stem
    tb_dir_path = str(tb_dir)
    tb_name = 'tb_common'
    tb_filename = tb_name + '.v'
    tb_path = str(tb_dir / tb_filename)
    dut_path = gen_apb2lb(tmpdir)

    sim = Simulator(simtool)
    sim.incdirs += [tb_dir_path]
    sim.sources += [tb_path, dut_path]
    sim.top = tb_name
    retval = sim.run(gui)
    if validate:
        assert '!@# TEST PASSED #@!' in sim.stdout


if __name__ == '__main__':
    tmpdir = tempfile.gettempdir()
    test_common(tmpdir, 'icarus', gui=True, validate=False)
