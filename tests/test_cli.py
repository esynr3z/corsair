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


class TestCLI:
    """Command line interface testing."""

    @pytest.fixture()
    def test_data_dir(self):
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

    def test_no_args(self, capsys):
        """Application with no arguments should show help and exit with no errors."""
        exit_code = self._run_cli([])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'usage: corsair' in captured.out

    def test_wrong_csr(self, capsys):
        """Application with wrong CSR should exit with error."""
        exit_code = self._run_cli(['aaa'])
        captured = capsys.readouterr()
        assert exit_code == 2
        assert 'corsair: error:' in captured.err

    def test_read_csr(self, test_data_dir, capsys):
        """Application with correct CSR should exit without error."""
        csr_file = test_data_dir.join('map.json')
        exit_code = self._run_cli([str(csr_file)])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'Read register map ... OK' in captured.out

    def test_chain_convert(self, test_data_dir, tmpdir):
        """Application should do the conversion: original CSR -> YAML -> JSON."""
        csr_file = test_data_dir.join('map.json')
        output_json = tmpdir.join('map_out.json')
        output_yaml = tmpdir.join('map_out.yaml')
        self._run_cli([str(csr_file), '--yaml=%s' % output_yaml])
        self._run_cli([str(output_yaml), '--json=%s' % output_json])
        orig_rmap = corsair.JSONReader()(str(csr_file))
        test_rmap = corsair.JSONReader()(str(output_json))
        assert orig_rmap == test_rmap

    def test_multiple_write(self, test_data_dir, tmpdir):
        """Application should create JSON and YAML outputs from input CSR file."""
        csr_file = test_data_dir.join('map.json')
        output_json = tmpdir.join('map_out.json')
        output_yaml = tmpdir.join('map_out.yaml')
        self._run_cli([str(csr_file), '--yaml=%s' % output_yaml, '--json=%s' % output_yaml])
        self._run_cli([str(output_yaml), '--json=%s' % output_json])
        orig_rmap = corsair.JSONReader()(str(csr_file))
        json_rmap = corsair.JSONReader()(str(output_json))
        yaml_rmap = corsair.YAMLReader()(str(output_yaml))
        assert orig_rmap == json_rmap == yaml_rmap
