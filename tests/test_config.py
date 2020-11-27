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
