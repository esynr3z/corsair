#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module to operate with Corsair configuration files
"""

from . import utils
import configparser


def default_globcfg():
    """Create a global configuration with parameters by default."""
    return {
        "base_address": 0,
        "data_width": 32,
        "address_width": 16,
        "register_reset": "sync_pos",
        "address_increment": "none",
        "address_alignment": "data_width",
        "force_name_case": "none",
    }


def read_csrconfig(cfgpath):
    """Parse Corsair configuration file. Return two dictionaries: global configuration and targets."""
    # open config file
    cfg = configparser.ConfigParser()
    cfg.read_file(open(cfgpath, 'r'))

    # parse global config
    globcfg = default_globcfg()
    if 'globcfg' in cfg.sections():
        globcfg.update(dict(cfg['globcfg']))
        globcfg["base_address"] = utils.str2int(globcfg["base_address"])
        globcfg["data_width"] = utils.str2int(globcfg["data_width"])
        globcfg["address_width"] = utils.str2int(globcfg["address_width"])
        try:
            globcfg["address_increment"] = utils.str2int(globcfg["address_increment"])
        except ValueError:
            pass
        try:
            globcfg["address_alignment"] = utils.str2int(globcfg["address_alignment"])
        except ValueError:
            pass
        validate_globcfg(globcfg)

    # parse targets
    targets = {}
    for target_name in [name for name in cfg.sections() if name != 'globcfg']:
        if 'generator' in dict(cfg[target_name]).keys():
            targets[target_name] = dict(cfg[target_name])

    return globcfg, targets


def write_csrconfig(cfgpath, globcfg, targets):
    """Save Corsair configuration file."""
    cfg = configparser.ConfigParser()
    data = {'globcfg': globcfg}
    data.update(targets)
    cfg.read_dict(data)
    cfg.write(open(cfgpath, 'w'))


def validate_globcfg(globcfg):
    """Validate a dictionary with global configuration."""
    # base_address
    assert utils.is_non_neg_int(globcfg["base_address"]), \
        "Wrong value for 'base_address'='%s'. Must be a non negative integer." % globcfg["base_address"]

    # data_width
    assert utils.is_non_neg_int(globcfg["data_width"]), \
        "Wrong value for 'data_width'='%s'. Must be a non negative integer." % globcfg["data_width"]

    # address_width
    assert utils.is_non_neg_int(globcfg["address_width"]), \
        "Wrong value for 'address_width'='%s'. Must be a non negative integer." % globcfg["address_width"]

    # register_reset
    register_reset_allowed = ['sync_pos', 'sync_neg', 'async_pos', 'async_neg']
    assert globcfg["register_reset"] in register_reset_allowed, \
        "Wrong value for 'register_reset'='%s'. Must be one of this: %s." % (globcfg["address_width"],
                                                                             register_reset_allowed)

    # address_increment
    address_increment_alowed = ['none', 'data_width']
    try:
        is_valid = (globcfg["address_increment"] in address_increment_alowed or
                    utils.is_non_neg_int(globcfg["address_increment"]))
    except ValueError:
        is_valid = False
    assert is_valid, \
        "Wrong value for 'address_increment'='%s'. Must be one of this: %s or a non negative integer." % (
            globcfg["address_increment"], address_increment_alowed)

    # address_alignment
    address_alignment_alowed = ['none', 'data_width']
    try:
        is_valid = (globcfg["address_alignment"] in address_alignment_alowed or
                    utils.is_non_neg_int(globcfg["address_alignment"]))
    except ValueError:
        is_valid = False
    assert is_valid, \
        "Wrong value for 'address_alignment'='%s'. Must be one of this: %s or a non negative integer." % (
            globcfg["address_alignment"], address_alignment_alowed)

    # force_name_case
    force_name_case_allowed = ['lower', 'upper', 'none']
    assert globcfg["force_name_case"] in force_name_case_allowed, \
        "Wrong value for 'force_name_case'='%s'. Must be one of this: %s." % (globcfg["force_name_case"],
                                                                              force_name_case_allowed)


globcfg = default_globcfg()


def set_globcfg(globcfg_):
    """Use specified global configuration for all operations"""
    global globcfg
    validate_globcfg(globcfg_)
    globcfg = globcfg_
