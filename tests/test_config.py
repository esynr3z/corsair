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
        print(p)
        print(repr(p))
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
            p = Parameter("param_a", 'aaa', checker=lambda val: val in ['bbb', 'ccc'])

    def test_min(self):
        """Test of a parameter min check"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 5, checker=lambda val: val >= 0xF)

    def test_max(self):
        """Test of a parameter max check"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 32, checker=lambda val: val < 32)

    def test_range_less(self):
        """Test of a parameter range check: if value is less"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 5, checker=lambda val: 100 <= val < 200)

    def test_range_greater(self):
        """Test of a parameter range check: if value is greater"""
        with pytest.raises(ValueError):
            p = Parameter("param_a", 300, checker=lambda val: 100 <= val < 200)


class TestParameterGroup:
    """Class 'ParameterGroup' testing"""
    def test_create(self):
        """Test of a parameter group creation"""
        p1_name = 'param_a'
        p1_val = 42
        p2_name = 'param_b'
        p2_val = 'value_b'
        p3_name = 'param_c'
        p3_val = True
        params = [
            Parameter(p1_name, p1_val),
            Parameter(p2_name, p2_val),
            Parameter(p3_name, p3_val)
        ]

        pg_name = 'group_a'
        pg = ParameterGroup(pg_name)
        pg.add_params(params)
        print(pg)
        assert pg.name == pg_name and pg[p2_name].value == p2_val

    def test_add_single_param(self):
        """Test of adding a parameter to a group"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        pg = ParameterGroup('group_a')
        pg.add_params(p1)
        print(pg)
        assert pg[p1_name].value == p1_val

    def test_add_multiple_param(self):
        """Test of adding a parameter to a group"""
        p1_name = 'param_a'
        p1_val = 42
        p1_name = 'param_a'
        p1_val = 42
        p2_name = 'param_b'
        p2_val = 'value_b'
        p1 = Parameter(p1_name, p1_val)
        p2 = Parameter(p2_name, p2_val)
        pg = ParameterGroup('group_a')
        pg.add_params([p1, p2])
        print(pg)
        assert pg[p2_name].value == p2_val

    def test_add_twice(self):
        """Test of adding a parameter to a group twice"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        pg = ParameterGroup('group_a')
        pg.add_params(p1)
        with pytest.raises(KeyError):
            pg.add_params(p1)


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
        pg = ParameterGroup(pg_name)
        pg.add_params([p1, p2])
        p3_name = 'param_c'
        p3_val = True
        p3 = Parameter(p3_name, p3_val)
        config = Configuration()
        config.add_params([pg, p3])
        print(config)
        assert config[pg_name][p1_name].value == p1_val and config[p3_name].value == p3_val

    def test_add_single_param(self):
        """Test of adding a parameter to the configuration"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        config = Configuration()
        config.add_params(p1)
        print(config)
        assert config[p1_name].value == p1_val

    def test_add_multiple_param(self):
        """Test of adding a parameter to a group"""
        p1_name = 'param_a'
        p1_val = 42
        p1_name = 'param_a'
        p1_val = 42
        p2_name = 'param_b'
        p2_val = 'value_b'
        p1 = Parameter(p1_name, p1_val)
        p2 = Parameter(p2_name, p2_val)
        config = Configuration()
        config.add_params([p1, p2])
        print(config)
        assert config[p2_name].value == p2_val

    def test_add_group(self):
        """Test of adding a parameter group to the configuration"""
        p1_name = 'param_a'
        p1_val = 42
        p1 = Parameter(p1_name, p1_val)
        p2_name = 'param_b'
        p2_val = 'value_b'
        p2 = Parameter(p2_name, p2_val)
        pg_name = 'group_a'
        pg = ParameterGroup(pg_name)
        pg.add_params([p1, p2])
        config = Configuration()
        config.add_params(pg)
        p3_name = 'param_c'
        p3_val = True
        p3 = Parameter(p3_name, p3_val)
        config[pg_name].add_params(p3)
        print(config)
        assert config[pg_name][p3_name].value == p3_val

    def test_set_values(self):
        """Test of loading new values to a configuration"""
        config = Configuration()
        new_values = {
            'read_filler': 42,
            'address_calculation': {
                'auto_increment_mode': 'custom',
                'auto_increment_value': 16
            },
            'parameter_a': 777,
            'group_a': {
                'par_deafbeef': 55,
                'group_b': {
                    'cafe': 'noname',
                    'address': 68,
                }
            }
        }
        config.values = new_values
        print(config)
        assert new_values['read_filler'] == config['read_filler'].value and \
               new_values['address_calculation']['auto_increment_mode'] == \
               config['address_calculation']['auto_increment_mode'].value and \
               new_values['group_a'] == config['group_a'].values

    def test_address_calculation_checker(self):
        config = Configuration()
        # no exception here
        print(config['address_calculation']['auto_increment_mode'])
        config['address_calculation']['auto_increment_mode'].value = 'data_width'
        print(config['address_calculation']['auto_increment_mode'])
        # exception on not allowed value
        with pytest.raises(ValueError):
            config['address_calculation']['auto_increment_mode'].value = 'lalala'

    def test_interface_generic_checker(self):
        config = Configuration()
        # no exception here
        print(config['interface_generic']['type'])
        print(config['interface_generic']['data_width'])
        config['interface_generic']['data_width'].value = 8
        print(config['interface_generic']['data_width'])
        config['interface_generic']['data_width'].value = 32
        print(config['interface_generic']['data_width'])
        # change interface type
        config['interface_generic']['type'].value = 'apb'
        print(config['interface_generic']['type'])
        # exception on not allowed value
        with pytest.raises(ValueError):
            config['interface_generic']['data_width'].value = 64
