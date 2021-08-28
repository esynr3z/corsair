#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bit field module tests
"""

import pytest
from corsair import EnumValue
import copy


def test_create():
    """Test of a enum creation."""
    # create with defaults
    enum = EnumValue()
    enum.validate()

    # create with non-default values
    name = 'OK'
    description = 'Ok'
    value = 1
    enum = EnumValue(name=name, description=description, value=value)
    print(repr(enum))
    print(enum)
    assert ((name, description, value) == (enum.name, enum.description, enum.value))


def test_eq():
    """Test of (non)equality comparision of enums."""
    e1 = EnumValue('AA', value=2)
    e2 = copy.deepcopy(e1)
    assert e1 == e2
    e2.value = 3
    assert e1 != e2


def test_name():
    """Name property"""
    # init
    enum = EnumValue(name='abc')
    assert enum.name == 'abc'
    # set
    enum.name = 'cde'
    assert enum.name == 'cde'
    # set wrong
    with pytest.raises(ValueError):
        enum.name = 5


def test_description():
    """Description property"""
    # init
    enum = EnumValue(description='abc')
    assert enum.description == 'abc'
    # set
    enum.description = 'cde'
    assert enum.description == 'cde'
    # set wrong
    with pytest.raises(ValueError):
        enum.description = 5


def test_value():
    """Value property"""
    # init
    enum = EnumValue(value=0x5)
    assert enum.value == 0x5
    enum = EnumValue(value='0x5')
    assert enum.value == 0x5
    # set
    enum.value = 0x3
    assert enum.value == 0x3
    enum.value = '0x6'
    assert enum.value == 0x6
    # set wrong
    with pytest.raises(ValueError):
        enum.value = 'zz'
    enum.value = -5
    with pytest.raises(AssertionError):
        enum.validate()


def test_custom_props():
    """Add custom properties on creation"""
    # init
    enum = EnumValue()
    assert enum.etc == {}
    enum = EnumValue(the_answer=42)
    assert enum.etc['the_answer'] == 42
    assert enum.as_dict()['the_answer'] == 42
