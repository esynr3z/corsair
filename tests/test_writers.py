#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers module tests.
"""

import pytest
from corsair import CsrJsonReader, CsrYamlReader
from corsair import CsrJsonWriter, CsrYamlWriter


class TestCsrJsonWriter:
    """Class 'CsrJsonWriter' testing."""

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
        reader = CsrJsonReader()
        rmap_orig = reader(input_file)
        # write RegisterMap to a JSON file
        writer = CsrJsonWriter()
        writer(output_file, rmap_orig)
        # read CSR map again and verify
        rmap_test = reader(output_file)
        assert rmap_test == rmap_orig


class TestCsrYamlWriter:
    """Class 'CsrYamlWriter' testing."""

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
        reader = CsrYamlReader()
        rmap_orig = reader(input_file)
        # write RegisterMap to a YAML file
        writer = CsrYamlWriter()
        writer(output_file, rmap_orig)
        # read CSR map again and verify
        rmap_test = reader(output_file)
        assert rmap_test == rmap_orig
