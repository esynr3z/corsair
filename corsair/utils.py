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


def is_non_neg_int(val, err_msg=""):
    if isinstance(val, int) and val >= 0:
        return True
    else:
        raise ValueError("Value of '%s' must be a non-negative integer." % val if not err_msg else err_msg)


def is_pos_int(val, err_msg=""):
    if isinstance(val, int) and val > 0:
        return True
    else:
        raise ValueError("Value of '%s' must be a positive integer." % val if not err_msg else err_msg)


def listify(obj):
    """Make lists from single objects. No changes are made for the argument of the 'list' type."""
    if type(obj) is not list:
        return [obj]
    else:
        return obj


def try_int_to_str(val, max_dec=1024):
    """Make string from int. Hexademical representaion will be used if input value greater that 'max_dec'."""
    if isinstance(val, int):
        if val > max_dec:
            return "0x%x" % val
        else:
            return "%d" % val
    else:
        return val
