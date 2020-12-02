#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration module tests.
"""

import pytest
from corsair.utils import *


def test_hex_to_dec():
    """Test of hex_to_dec() function"""
    assert hex_to_dec('0xdeadbeef') == 0xdeadbeef


def test_try_hex_to_dec():
    """Test of try_hex_to_dec() function"""
    in_val = [5, 6, 'a', '0x55', 'ff', '0x06', 'zzzz']
    out1_val = [try_hex_to_dec(v) for v in in_val]
    out2_val = [try_hex_to_dec(v, prefix='') for v in in_val]
    golden1_val = [5, 6, 'a', 0x55, 'ff', 0x06, 'zzzz']
    golden2_val = [5, 6, 0xa, 0x55, 0xff, 0x06, 'zzzz']
    assert out1_val == golden1_val and out2_val == golden2_val


def test_tree_hex_to_dec():
    """Test of tree_hex_to_dec() function"""
    test_tree = {'test': [0, 5, 'abcz', '0x55', ['ff', '0xf', {'a': 5, 'b': '0x0'}]]}
    golden_tree = {'test': [0, 5, 'abcz', 0x55, ['ff', 0xf, {'a': 5, 'b': 0x0}]]}
    tree_hex_to_dec(test_tree)
    assert test_tree == golden_tree
