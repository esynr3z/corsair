#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers module tests.
"""

import pytest
from corsair import RegisterMapReader, ConfigurationReader
from corsair import RegisterMapWriter, ConfigurationWriter, LbBridgeWriter
from corsair import HdlWriter, DocsWriter
from corsair import Configuration, RegisterMap


class TestRegisterMapWriter:
    """Class 'RegisterMapWriter' testing."""

    def _write(self, path):
        # create regmap
        rmap_orig = RegisterMap()
        # write to file
        RegisterMapWriter()(path, rmap_orig)
        # read back
        rmap_test = RegisterMapReader()(path)
        assert rmap_test == rmap_orig

    def test_write_json(self, tmpdir):
        """Test of writing register map to a JSON file."""
        output_file = str(tmpdir.join('map_out.json'))
        print('output_file:', output_file)
        self._write(output_file)

    def test_write_yaml(self, tmpdir):
        """Test of writing register map to a YAML file."""
        output_file = str(tmpdir.join('map_out.yaml'))
        print('output_file:', output_file)
        self._write(output_file)


class TestConfigurationWriter:
    """Class 'ConfigurationWriter' testing."""

    def _write(self, path):
        # create config
        config_orig = Configuration()
        # write to file
        ConfigurationWriter()(path, config_orig)
        # read back
        config_test = ConfigurationReader()(path)
        assert config_orig == config_test

    def test_write_json(self, tmpdir):
        """Test of writing configuration to a JSON file."""
        output_file = str(tmpdir.join('config_out.json'))
        print('output_file:', output_file)
        self._write(output_file)

    def test_write_yaml(self, tmpdir):
        """Test of writing configuration to a YAML file."""
        output_file = str(tmpdir.join('config_out.yaml'))
        print('output_file:', output_file)
        self._write(output_file)


class TestLbBridgeWriter:
    """Class 'LbBridgeWriter' testing."""

    def test_apb_write(self, tmpdir):
        """Test of creating bridge to LocalBus module in Verilog."""
        output_file = str(tmpdir.join('apb2lb.v'))
        print('output_file:', output_file)
        # create configuration
        config = Configuration()
        config['lb_bridge']['type'].value = 'apb'
        # write output file
        writer = LbBridgeWriter()
        writer(output_file, config)
        # read file and verify
        with open(output_file, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert 'APB to Local Bus bridge' in raw_str


class TestHdlWriter:
    """Class 'HdlWriter' testing."""

    def test_verilog_write(self, tmpdir):
        """Test of creating regmap module in Verilog."""
        output_file = str(tmpdir.join('regs.v'))
        print('output_file:', output_file)
        # create regmap
        rmap = RegisterMap()
        # write output file
        writer = HdlWriter()
        writer(output_file, rmap)
        # read file and verify
        with open(output_file, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert 'module regs' in raw_str
        assert 'endmodule' in raw_str


class TestDocsWriter:
    """Class 'DocsWriter' testing."""

    def _read_rmap(self, path):
        reader = RegisterMapReader()
        rmap = reader(path)

    def test_md_write(self, tmpdir):
        """Test of creating markdown regmap file."""
        rmap_path = 'tests/data/map.json'
        md_path = str(tmpdir.join('regs.md'))
        print('rmap_path:', rmap_path)
        print('md_path:', md_path)
        # read regmap
        rmap = RegisterMapReader()(rmap_path)
        # write output file
        DocsWriter()(md_path, rmap)
        # read file and verify
        with open(md_path, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert '## Register map' in raw_str
        assert 'Back to [Register map](#register-map).' in raw_str
