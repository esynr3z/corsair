#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Readers module tests.
"""

import pytest
from corsair import CsrJsonReader, CsrYamlReader


class TestJsonReader:
    """Class 'CsrJsonReader' testing."""

    @pytest.fixture()
    def input_file(self):
        return 'tests/data/map.json'

    def test_read(self, input_file):
        """Test of reading JSON file with CSR map."""
        print('input_file:', input_file)
        reader = CsrJsonReader()
        rmap = reader(input_file)
        print(rmap.config)
        print(rmap)
        assert rmap.config['read_filler'].value == 0xDEADBEEF
        assert rmap['LEN'].address == 0x0
        assert rmap['START']['STB'].access == 'wo'


class TestYamlReader:
    """Class 'CsrYamlReader' testing."""

    @pytest.fixture()
    def input_file(self):
        return 'tests/data/map.yml'

    def test_read(self, input_file):
        """Test of reading YAML file with CSR map."""
        print('input_file:', input_file)
        reader = CsrYamlReader()
        rmap = reader(input_file)
        print(rmap.config)
        print(rmap)
        assert rmap.config['read_filler'].value == 0xDEADBEEF
        assert rmap['LEN'].address == 0x0
        assert rmap['START']['STB'].access == 'wo'
