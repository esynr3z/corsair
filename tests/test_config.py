#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration module tests.
"""

import pytest
from corsair.config import (
    Parameter,
    ParameterGroup,
    Configuration
)


class TestParameter:
    """Class 'Parameter' testing"""
    def test_create(self):
        """Test of a parameter creation"""
        p_name = "param_a"
        p_val = 42
        p = Parameter(p_name, p_val)
        print(str(p))
        assert p.name == p_name and p.value == p_val

    def test_modify(self):
        """Test of a parameter creation"""
        p = Parameter("param_a", 42)
        p_new_val = 'hello'
        p.value = p_new_val
        assert p.value == p_new_val

    def test_allowlist(self):
        """Test of a parameter allowlist check"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 'aaa', allowlist=['bbb', 'ccc'])

    def test_min(self):
        """Test of a parameter min check"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 5, min=0xF)

    def test_max(self):
        """Test of a parameter max check"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 32, max=32)

    def test_range_less(self):
        """Test of a parameter range check: if value is less"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 5, min=100, max=200)

    def test_range_greater(self):
        """Test of a parameter range check: if value is greater"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 300, min=100, max=200)


class TestParameterGroup:
    """Class 'ParameterGroup' testing"""
    def test_create(self):
        """Test of a parameter group creation"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        p2_name = 'param_b'
        p2_val = 'value_b'
        p2 = Parameter(p2_name, p2_val)
        p3_name = 'param_c'
        p3_val = True
        p3 = Parameter(p3_name, p3_val)
        pg_name = 'group_a'
        pg = ParameterGroup(pg_name, [p1, p2, p3])
        print(str(pg))
        assert pg.name == pg_name and pg[p2_name] == p2_val

    def test_add_param(self):
        """Test of adding a parameter to a group"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        pg = ParameterGroup('group_a')
        pg.add_param(p1)
        print(str(pg))
        assert pg[p1_name] == p1_val


class TestConfiguration:
    """Class 'Configuration' testing"""
    def test_create(self):
        """Test of a configuration creation"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        p2_name = 'param_b'
        p2_val = 'value_b'
        p2 = Parameter(p2_name, p2_val)
        pg_name = 'group_a'
        pg = ParameterGroup(pg_name, [p1, p2])
        p3_name = 'param_c'
        p3_val = True
        p3 = Parameter(p3_name, p3_val)
        config = Configuration([pg, p3])
        print(str(config))
        assert config[pg_name][p1_name] == p1_val and config[p3_name] == p3_val

    def test_add_param(self):
        """Test of adding a parameter to the configuration"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        config = Configuration()
        config.add_param(p1)
        print(str(config))
        assert config[p1_name] == p1_val

    def test_add_group(self):
        """Test of adding a parameter group to the configuration"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        p2_name = 'param_b'
        p2_val = 'value_b'
        p2 = Parameter(p2_name, p2_val)
        pg_name = 'group_a'
        pg = ParameterGroup(pg_name, [p1, p2])
        config = Configuration()
        config.add_param(pg)
        p3_name = 'param_c'
        p3_val = True
        p3 = Parameter(p3_name, p3_val)
        config[pg_name].add_param(p3)
        print(str(config))
        assert config[pg_name][p3_name] == p3_val
