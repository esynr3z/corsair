#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions and classes.
"""


def hex_to_dec(val):
    """Converts hexademical string to integer"""
    return int(val, 16)


def try_hex_to_dec(val, prefix='0x'):
    """Tries to convert hexademical string to integer. Returns original value if not possible."""
    try:
        # convert only if prefixes match
        if prefix in val[:len(prefix)]:
            return hex_to_dec(val)
    except (TypeError, ValueError):
        pass
    return val


def tree_hex_to_dec(tree):
    """Recursevely convert only '0x' hexademical strings to integers inside list or dict in-place."""
    for idx, val in enumerate(tree) if isinstance(tree, list) else tree.items():
        if isinstance(val, (dict, list)):
            tree_hex_to_dec(val)
        else:
            tree[idx] = try_hex_to_dec(val)
