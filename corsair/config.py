#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration module.

More information about configuration options can be found in docs/config.md.
"""

from . import utils


class Parameter():
    """Generic parameter.

    Attributes:
        name: Name of the parameter.
        value: Value of the parameter.
        checker: Lambda function to perform value checking.

    """
    def __init__(self, name, value=None, checker=lambda val: True):
        """Initialize parameter.

        Args:
            name: String with the parameter's name.
            value (optional): Value of the parameter.
            checker (optional):
                Lambda function to perform value checking.
                Returns True if value check is OK, and False otherwise.

        Raises:
            ValueError: An error occured if value does not match checker rules.

        """
        self._value = None

        self.name = name
        self.checker = checker
        self.value = value

    def __repr__(self):
        """Returns string representation of an object."""
        return 'Parameter(%s, %s)' % (repr(self.name), repr(self.value))

    def __str__(self):
        """Returns 'informal' string representation of an object."""
        return self._str()

    def _str(self, indent=''):
        """Returns indented parameter's string with name and value."""
        return indent + '%s: %s' % (self.name, self._value)

    @property
    def value(self):
        """Current value of the parameter.

        Raises:
            ValueError: An error occured if value fails the check after set.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        # store all 0x-like hexademical strings as integers if possible
        self._value = utils.try_hex_to_dec(new_value)
        # run checker for the new value
        self._check()

    def _check(self):
        """Check parameter value correctness.

        Raises:
            ValueError: An error occured if value does not match checker rules.
        """
        if self.checker(self.value) is False:
            raise ValueError('"%s" parameter with "%s" value failed the check!' % (self.name,
                                                                                   self.value))


class ParameterGroup():
    """Group of parameters or other groups.

    Attributes:
        name: Name of the group.
        names: List with all the objects (parameters/groups) names
        params: List with all the objects
        values: Dictionary with the values of the parameters/groups.
    """
    def __init__(self, name):
        """Initialize parameter group."""
        self.name = name
        self._params = {}

    def __repr__(self):
        """Returns string representation of an object."""
        return 'ParameterGroup(%s)' % repr(self.name)

    def __str__(self):
        """Returns 'informal' string representation of an object."""
        return self._str()

    def __getitem__(self, key):
        """Get parameter or group by name.

        Raises:
            KeyError: An error occured if parameter or group does not exists.
        """
        try:
            return self._params[key]
        except KeyError:
            raise KeyError("Parameter/Group with a name '%s' doesn't exist!" % key)

    def __setitem__(self, key, value):
        """Set parameter or group by name"""
        raise KeyError("Not able to set '%s' item directly in '%s' group!"
                       " Try use add_params() method." % (key, self.name))

    def _str(self, indent=''):
        """Returns indented string with group members and their values"""
        new_indent = indent + '  '
        params = [self[name]._str(new_indent) for name in self.names]
        params_str = '\n'.join(params) if params else new_indent + 'empty'
        return indent + '%s:\n' % self.name + params_str

    @property
    def names(self):
        """Return all parameters names"""
        return self._params.keys()

    @property
    def params(self):
        """Returns list with parameters objects."""
        return [param for param in self._params.items()]

    def add_params(self, new_params):
        """Add parameters."""
        # hack to handle single elements
        if type(new_params) is not list:
            new_params = [new_params]

        # add params to dict one by one
        for p in new_params:
            if p.name in self._params:
                raise KeyError("Item with name '%s' is already present in '%s' group!" % (p.name, self.name))
            self._params[p.name] = p

    @property
    def values(self):
        """Dictionary with values of the parameters/groups.

        Getter:
            Returns dictionary with pairs {name:value} of all parameter/groups of the current group.

        Setter:
            Sets only parameters/groups specified in the input dictionary,
            but if parameter/group does not exist, it will create it.
        """
        values = {}
        for name in self.names:
            if isinstance(self[name], ParameterGroup):
                values[name] = self[name].values
            else:
                values[name] = self[name].value
        return values

    @values.setter
    def values(self, new_values):
        for name in new_values.keys():
            try:
                # if parameter/group exists
                if isinstance(self[name], ParameterGroup):
                    self[name].values = new_values[name]
                else:
                    self[name].value = new_values[name]
            except KeyError:
                # else if parameter/group does not exists
                if isinstance(new_values[name], dict):
                    self.add_params(ParameterGroup(name=name))
                    self[name].values = new_values[name]
                else:
                    self.add_params(Parameter(name=name, value=new_values[name]))


class Configuration(ParameterGroup):
    """Collection of global parameters."""
    def __init__(self):
        """Initialize configuration."""
        super().__init__('configuration')
        self._init_default_params()

    def __repr__(self):
        """Returns string representation of an object."""
        return 'Configuration()'

    def _init_default_params(self):
        """Initalize all default params"""

        # parameter read_filler
        self.add_params(Parameter(name='read_filler', value=0x0))

        # group address_calculation
        self.add_params(ParameterGroup('address_calculation'))

        self['address_calculation'].add_params([
            Parameter(name='auto_increment_mode', value='none',
                      checker=lambda val: val in ['none', 'data_width', 'custom']),
            Parameter(name='auto_increment_value', value=4, checker=lambda val: val >= 1),
            Parameter(name='alignment_mode', value='data_width',
                      checker=lambda val: val in ['none', 'data_width', 'custom']),
            Parameter(name='alignment_value', value=4, checker=lambda val: val >= 1)
        ])

        # parameter register_reset
        reg_rst_allowlist = ['sync_pos', 'sync_neg', 'async_pos', 'async_neg', 'init_only']
        self.add_params(Parameter(name='register_reset', value='sync_pos',
                                  checker=lambda val: val in reg_rst_allowlist))

        # group interface_generic
        self.add_params(ParameterGroup('interface_generic'))

        ifgen_type_allowed = ['amm', 'apb', 'axil', 'lb']
        self['interface_generic'].add_params(
            Parameter(name='type', value='lb', checker=lambda val: val in ifgen_type_allowed)
        )

        ifgen_data_width_allowed = {
            'amm': [8, 16, 32, 64, 128, 256, 512, 1024],
            'apb': [8, 16, 32],
            'axil': [32, 64],
            'lb': [8, 16, 32, 64, 128, 256, 512, 1024]
        }
        ifgen_addr_width_allowed = {
            'amm': range(1, 64),
            'apb': range(1, 32),
            'axil': [32, 64],
            'lb': range(1, 64)
        }
        self['interface_generic'].add_params([
            Parameter(name='data_width', value=32,
                      checker=lambda val: val in ifgen_data_width_allowed[self['interface_generic']['type'].value]),
            Parameter(name='address_width', value=32,
                      checker=lambda val: val in ifgen_addr_width_allowed[self['interface_generic']['type'].value])
        ])

        # group interface_specific
        self.add_params(ParameterGroup('interface_specific'))
