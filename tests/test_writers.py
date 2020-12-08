#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers module tests.
"""

import pytest
from corsair.readers import JSONReader, YAMLReader
from corsair.writers import JSONWriter, YAMLWriter


class TestJSONWriter:
    """Class 'JSONWriter' testing."""

    @pytest.fixture()
    def input_file(self):
        return 'tests/data/map.json'

    @pytest.fixture()
    def output_file(self, tmpdir):
        return tmpdir.join('map_out.json')

    def test_write(self, input_file, output_file):
        """Test of writing CSR map to a JSON file."""
        print('input_file:', input_file)
        print('output_file:', output_file)
        # read some CSR map
        reader = JSONReader()
        rmap_orig = reader(input_file)
        # write RegisterMap to a JSON file
        writer = JSONWriter()
        writer(output_file, rmap_orig)
        # read CSR map again and verify
        rmap_test = reader(output_file)
        assert rmap_test == rmap_orig


class TestYAMLWriter:
    """Class 'YAMLWriter' testing."""

    @pytest.fixture()
    def input_file(self):
        return 'tests/data/map.yml'

    @pytest.fixture()
    def output_file(self, tmpdir):
        return tmpdir.join('map_out.yml')

    def test_write(self, input_file, output_file):
        """Test of writing CSR map to a YAML file."""
        print('input_file:', input_file)
        print('output_file:', output_file)
        # read some CSR map
        reader = YAMLReader()
        rmap_orig = reader(input_file)
        # write RegisterMap to a YAML file
        writer = YAMLWriter()
        writer(output_file, rmap_orig)
        # read CSR map again and verify
        rmap_test = reader(output_file)
        assert rmap_test == rmap_orig
