#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generators module tests
"""

import pytest
from corsair import RegisterMap, generators, config, utils


class TestJson:
    """Class 'generators.Json' testing."""

    def test_dump(self, tmpdir):
        """Test of writing register map to a JSON file"""
        output_file = str(tmpdir.join('map_out.json'))
        print('output_file:', output_file)
        # create regmap
        rmap = utils.create_template()
        rmap[0].etc['the_answer'] = 42
        # write to file
        generators.Json(rmap, output_file).generate()
        # read back
        rmap_test = RegisterMap()
        rmap_test.read_file(output_file)
        assert rmap_test == rmap
        assert rmap[0].etc['the_answer'] == rmap_test[0].etc['the_answer'] == 42


class TestYaml:
    """Class 'generators.Yaml' testing."""

    def test_dump(self, tmpdir):
        """Test of writing register map to a YAML file"""
        output_file = str(tmpdir.join('map_out.yaml'))
        print('output_file:', output_file)
        # create regmap
        rmap = utils.create_template()
        rmap[0].etc['the_answer'] = 42
        # write to file
        generators.Yaml(rmap, output_file).generate()
        # read back
        rmap_test = RegisterMap()
        rmap_test.read_file(output_file)
        assert rmap_test == rmap
        assert rmap[0].etc['the_answer'] == rmap_test[0].etc['the_answer'] == 42


class TestTxt:
    """Class 'generators.Txt' testing."""

    def test_txt(self, tmpdir):
        """Test of writing register map to a txt file"""
        # prepare output file
        output_file = str(tmpdir.join('map_out.txt'))
        print('output_file:', output_file)
        # create regmap
        rmap = utils.create_template_simple()
        # write to file
        generators.Txt(rmap, output_file).generate()
        # read back
        rmap_test = RegisterMap()
        rmap_test.read_file(output_file)
        assert rmap_test == rmap


class TestVerilog:
    """Class 'generators.Verilog' testing."""

    def test_verilog_write(self, tmpdir):
        """Test of creating regmap module in Verilog."""
        output_file = str(tmpdir.join('regs.v'))
        print('output_file:', output_file)
        # create regmap
        rmap = utils.create_template()
        # write output file
        generators.Verilog(rmap, output_file).generate()
        # read file and verify
        with open(output_file, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert 'module regs' in raw_str
        assert 'endmodule' in raw_str


class TestVerilogHeader:
    """Class 'generators.VerilogHeader' testing."""

    def test_vheader_write(self, tmpdir):
        """Test of creating Verilog header."""
        output_file = str(tmpdir.join('regs.vh'))
        print('output_file:', output_file)
        # create regmap
        rmap = utils.create_template()
        # write output file
        generators.VerilogHeader(rmap, output_file).generate()
        # read file and verify
        with open(output_file, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert '`define CSR_' in raw_str


class TestLbBridgeVerilog:
    """Class 'generators.LbBridgeVerilog' testing."""

    def _test(self, tmpdir, filename, bridge_type, assert_str):
        output_file = str(tmpdir.join(filename))
        print('output_file:', output_file)
        # write output file
        generators.LbBridgeVerilog(path=output_file, bridge_type=bridge_type).generate()
        # read file and verify
        with open(output_file, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert assert_str in raw_str

    def test_apb(self, tmpdir):
        """Test of creating APB to LocalBus module in Verilog"""
        self._test(tmpdir, 'apb2lb.v', 'apb', 'APB to Local Bus bridge')

    def test_amm(self, tmpdir):
        """Test of creating Avalon-MM to LocalBus module in Verilog"""
        self._test(tmpdir, 'amm2lb.v', 'amm', 'Avalon-MM to Local Bus bridge')

    def test_axil(self, tmpdir):
        """Test of creating AXI-Lite to LocalBus module in Verilog"""
        self._test(tmpdir, 'axil2lb.v', 'axil', 'AXI-Lite to Local Bus bridge')


class TestMarkdown:
    """Class 'generators.Markdown' testing."""

    def test_md(self, tmpdir):
        """Test of creating markdown regmap file."""
        md_path = str(tmpdir.join('regs.md'))
        print('md_path:', md_path)
        # create regmap
        rmap = utils.create_template()
        # write output file
        generators.Markdown(rmap, md_path).generate()
        # read file and verify
        with open(md_path, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert '## Register map' in raw_str
        assert 'Back to [Register map](#register-map-summary).' in raw_str


class TestPython:
    """Class 'generators.Python' testing."""

    def test_py(self, tmpdir):
        """Test of creating python regmap file."""
        py_path = str(tmpdir.join('regs.py'))
        print('py_path:', py_path)
        # create regmap
        rmap = utils.create_template()
        # write output file
        generators.Python(rmap, py_path).generate()
        # read file and verify
        with open(py_path, 'r') as f:
            raw_str = ''.join(f.readlines())
        assert 'class RegMap:' in raw_str
