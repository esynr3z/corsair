#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for corsair command line interface.
"""

import pytest
import os
import sys
from corsair.__main__ import main as corsair_main
from py._path.local import LocalPath
import corsair


class _TestCLI:
    @pytest.fixture()
    def datadir(self):
        return LocalPath('tests/data')

    def _run_cli(self, argv=[]):
        """Wrapper to run application with specified arguments and catch exit exception."""
        orig_argv = sys.argv
        sys.argv = [orig_argv[0]] + argv
        try:
            with pytest.raises(SystemExit) as e:
                corsair_main()
        finally:
            sys.argv = orig_argv
        return e.value.code


class TestCommon(_TestCLI):
    """Common tests for command line interface."""
    def test_no_args(self, capsys):
        """Application with no arguments should show help and exit with no errors."""
        exit_code = self._run_cli([])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'usage: corsair' in captured.out


class TestRegisterMap(_TestCLI):
    """Register map related testing."""
    def test_read(self, datadir, capsys):
        """Application with correct regmap should exit without error."""
        rmap_file = str(datadir.join('map.json'))
        exit_code = self._run_cli(['-r', rmap_file])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read registers ... OK' in captured.out

    def test_template(self, tmpdir, capsys):
        """Write template."""
        template = str(tmpdir.join('map.json'))
        exit_code = self._run_cli(['--template-regmap', template])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Save data to file ... OK' in captured.out
        # read back
        exit_code = self._run_cli(['--regmap', template])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read registers ... OK' in captured.out

    def test_convert(self, datadir, tmpdir, capsys):
        """Covert existing regmap to other format."""
        rmap_orig = str(datadir.join('map.json'))
        rmap_new = str(tmpdir.join('map.yaml'))
        exit_code = self._run_cli(['-r', rmap_orig, '--dump-regmap', rmap_new])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read registers ... OK' in captured.out
        assert 'Save data to file ... OK' in captured.out
        # read back
        exit_code = self._run_cli(['--regmap', rmap_new])
        assert exit_code == 0

    def test_create_hdl(self, datadir, tmpdir, capsys):
        """Create register map verilog regs.v file."""
        rmap_file = str(datadir.join('map.json'))
        exit_code = self._run_cli(['-r', rmap_file, '--output-dir', str(tmpdir.join('out')), '--hdl'])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read registers ... OK' in captured.out
        assert 'Save data to file ... OK' in captured.out


class TestConfig(_TestCLI):
    """Configuration related testing."""
    def test_read(self, datadir, capsys):
        """Application with correct regmap should exit without error."""
        config_file = str(datadir.join('config.json'))
        exit_code = self._run_cli(['-c', config_file])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read configuration ... OK' in captured.out

    def test_template(self, tmpdir, capsys):
        """Write template."""
        template = str(tmpdir.join('config.json'))
        exit_code = self._run_cli(['--template-config', template])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Save data to file ... OK' in captured.out
        # read back
        exit_code = self._run_cli(['--config', template])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read configuration ... OK' in captured.out

    def test_convert(self, datadir, tmpdir, capsys):
        """Convert existing config to other format."""
        config_orig = str(datadir.join('config.json'))
        config_new = str(tmpdir.join('config.yml'))
        exit_code = self._run_cli(['-c', config_orig, '--dump-config', config_new])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read configuration ... OK' in captured.out
        assert 'Save data to file ... OK' in captured.out
        # read back
        exit_code = self._run_cli(['--config', config_new])
        assert exit_code == 0


class TestLbBridge(_TestCLI):
    """LocalBus HDL module related testing."""
    def test_create_apb(self, tmpdir, capsys):
        """Create apb2lb_regs.v file."""
        # create register map file with configiration
        rmap = corsair.RegisterMap()
        rmap.config['name'].value = 'regs'
        rmap.config['lb_bridge']['type'].value = 'apb'
        rmap_file = str(tmpdir.join('map.json'))
        corsair.RegisterMapWriter()(rmap_file, rmap)
        # create bridge
        exit_code = self._run_cli(['-r', rmap_file, '--lb-bridge'])
        captured = capsys.readouterr()
        assert exit_code == 0
        # read file and verify
        lb_bridge_file = str(tmpdir.join('apb2lb_regs.v'))
        with open(lb_bridge_file, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert 'APB to Local Bus bridge' in raw_str


class TestDocs(_TestCLI):
    """Register nap documentation related testing."""

    def test_create_md(self, datadir, tmpdir, capsys):
        """Create register map documentation regs.md file."""
        rmap_file = str(datadir.join('map.json'))
        exit_code = self._run_cli(['-r', rmap_file, '--output-dir', str(tmpdir), '--docs'])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read registers ... OK' in captured.out
        assert 'Draw images ... OK' in captured.out
