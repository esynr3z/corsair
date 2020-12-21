#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers module tests.
"""

import pytest
from corsair import RegisterMapReader, ConfigurationReader
from corsair import RegisterMapWriter, ConfigurationWriter, LbBridgeWriter
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


class TestBridgeWriter:
    """Class 'BridgeWriter' testing."""

    @pytest.fixture()
    def output_file(self, tmpdir):
        return

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
