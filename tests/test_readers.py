#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Readers module tests.
"""

import pytest
from corsair.readers import JSONReader


class TestJSONReader:
    """Class 'JSONReader' testing."""

    @pytest.fixture()
    def json_file(self):
        return 'tests/data/map.json'

    def test_read(self, json_file):
        """Test of reading JSON file with CSR map."""
        reader = JSONReader()
        rmap = reader(json_file)
        print(rmap.config)
        print(rmap)
        assert rmap.config['read_filler'].value == 0xDEADBEEF and \
               rmap['LEN'].address == 0x0 and \
               rmap['START']['STB'].access == 'wo'
