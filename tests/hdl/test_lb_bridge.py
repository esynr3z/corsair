#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for generated bridges
"""

import sys
from attr.setters import convert
sys.path.insert(0, '../..')
import pytest
from sim import Simulator, CliArgs, path_join, parent_dir
import corsair


TEST_DIR = parent_dir(__file__)


def gen_bridge(tmpdir, bridge, reset):
    config = corsair.Configuration()
    config['lb_bridge']['type'].value = bridge
    config['register_reset'].value = reset
    bridge_path = path_join(tmpdir, '%s2lb.v' % bridge)
    corsair.LbBridgeWriter()(bridge_path, config)
    return (bridge_path, config)


@pytest.fixture()
def simtool():
    return 'modelsim'


@pytest.fixture(params=['apb', 'axil', 'amm', 'spi'])
def bridge(request):
    return request.param


@pytest.fixture(params=['sync_pos', 'sync_neg', 'async_pos', 'async_neg'])
def reset(request):
    return request.param


def test(tmpdir, bridge, reset, simtool, defines=[], gui=False, pytest_run=True):
    # create sim
    tb_dir = path_join(TEST_DIR, 'test_lb_bridge')
    beh_dir = path_join(TEST_DIR, 'beh')
    sim = Simulator(name=simtool, gui=gui, cwd=tmpdir)
    sim.incdirs += [tmpdir, tb_dir, beh_dir]
    sim.sources += [path_join(tb_dir, 'tb.sv')]
    sim.sources += beh_dir.glob('*.sv')
    sim.defines += defines
    sim.top = 'tb'
    sim.setup()
    # prepare test
    dut_src, dut_config = gen_bridge(tmpdir, bridge, reset)
    sim.sources += [dut_src]
    sim.defines += [
        'DUT_DATA_W=%d' % dut_config['data_width'].value,
        'DUT_ADDR_W=%d' % dut_config['address_width'].value,
        'DUT_%s' % bridge.upper(),
        'RESET_ACTIVE=%d' % ('pos' in reset),
    ]
    # run sim
    sim.run()
    if pytest_run:
        assert sim.is_passed


if __name__ == '__main__':
    # run script with key -h to see help
    cli = CliArgs(default_test='test')
    cli.args_parser.add_argument('--bridge', default='apb', metavar='<bridge>', dest='bridge',
                                 help="bridge <bridge> to LocalBus; default is 'apb'")
    cli.args_parser.add_argument('--reset', default='sync_pos', metavar='<reset>', dest='reset',
                                 help="reset <reset> for bridge registers; default is 'sync_pos'")
    args = cli.parse()
    try:
        globals()[args.test](tmpdir='work',
                             bridge=args.bridge,
                             reset=args.reset,
                             simtool=args.simtool,
                             gui=args.gui,
                             defines=args.defines,
                             pytest_run=False)
    except KeyError:
        print("There is no test with name '%s'!" % args.test)
