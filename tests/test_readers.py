#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Readers module tests.
"""

import pytest
from corsair import JSONReader, YAMLReader


class TestJSONReader:
    """Class 'JSONReader' testing."""

    @pytest.fixture()
    def input_file(self):
        return 'tests/data/map.json'

    def test_read(self, input_file):
        """Test of reading JSON file with CSR map."""
        print('input_file:', input_file)
        reader = JSONReader()
        rmap = reader(input_file)
        print(rmap.config)
        print(rmap)
        assert rmap.config['read_filler'].value == 0xDEADBEEF and \
               rmap['LEN'].address == 0x0 and \
               rmap['START']['STB'].access == 'wo'


class TestYAMLReader:
    """Class 'YAMLReader' testing."""

    @pytest.fixture()
    def input_file(self):
        return 'tests/data/map.yml'

    def test_read(self, input_file):
        """Test of reading YAML file with CSR map."""
        print('input_file:', input_file)
        reader = YAMLReader()
        rmap = reader(input_file)
        print(rmap.config)
        print(rmap)
        assert rmap.config['read_filler'].value == 0xDEADBEEF and \
               rmap['LEN'].address == 0x0 and \
               rmap['START']['STB'].access == 'wo'
