#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Readers module tests.
"""

import pytest
from corsair import RegisterMapReader, ConfigurationReader


class TestRegisterMapReader:
    """Class 'RegisterMapReader' testing."""

    def _read(self, path):
        reader = RegisterMapReader()
        rmap = reader(path)
        print(rmap.config)
        print(rmap)
        assert rmap.config['regmap']['read_filler'].value == 0xDEADBEEF
        assert rmap['LEN'].address == 0x0
        assert rmap['START']['STB'].access == 'wo'

    def test_read_json(self):
        """Test of reading JSON file."""
        input_file = 'tests/data/map.json'
        print('input_file:', input_file)
        self._read(input_file)

    def test_read_yaml(self,):
        """Test of reading YAML file."""
        input_file = 'tests/data/map.yaml'
        print('input_file:', input_file)
        self._read(input_file)


class TestConfigurationReader:
    """Class 'ConfigurationReader' testing."""

    def _read(self, path):
        reader = ConfigurationReader()
        config = reader(path)
        print(config)
        assert config['regmap']['read_filler'].value == 0xDEADBEEF

    def test_read_json(self):
        """Test of reading JSON file."""
        input_file = 'tests/data/config.json'
        print('input_file:', input_file)
        self._read(input_file)

    def test_read_yaml(self,):
        """Test of reading YAML file."""
        input_file = 'tests/data/config.yaml'
        print('input_file:', input_file)
        self._read(input_file)
