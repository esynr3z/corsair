#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration module.

More information about configuration options used in Configuration class
can be found in docs/configuration.md.
"""


class Parameter():
    """Generic parameter.

    Attributes:
      name: Name of the parameter.
      value: Value of the parameter.
      allowlist: List with values allowed for the parameter.
      min: Parameter value must be equal or greater than that number.
      max: Parameter value must be less than that number.

    """
    def __init__(self, name, value=None, allowlist=None, min=None, max=None):
        """Initialize parameter.

        Args:
          name: String with the parameter's name.
          value: Optional; Value of the parameter.
          allowlist: Optional;
            List with values allowed for the parameter.
            Should not be mixed with min, max arguments.
          min: Optional;
            Parameter value must be equal or greater than that number.
            Should not be mixed allowlist argument.
            Use it with max argument to create a range.
          max: Optional;
            Parameter value must be less than that number.
            Should not be mixed allowlist argument.
            Use it with min argument to create a range.

        Raises:
          ValueError: An error occured if value does not match allowlist or
            specified range (with min, max, min and max)

        """
        self.name = name
        self._value = value
        self.allowlist = allowlist
        self.min = min
        self.max = max
        if value is not None:
            self._check()

    def __str__(self):
        """Returns parameter's string"""
        return '%s: %s' % (self.name, self._value)

    @property
    def value(self):
        """Get current value"""
        return self._value

    @value.setter
    def value(self, new_value):
        """Set current value

        Raises:
          ValueError: An error occured if value does not match allowlist or
            specified range (with min, max, min and max)
        """
        self._value = new_value
        self._check()

    def _check(self):
        """Check parameter value correctness

        Raises:
          ValueError: An error occured if value does not match allowlist or
            specified range (with min, max, min and max)
        """
        if self.allowlist is not None:
            if self._value not in self.allowlist:
                raise ValueError('%s parameter has no option %s in %s!' % (self.name,
                                                                           self._value,
                                                                           self.allowlist))
        elif (self.min is not None) and (self.max is not None):
            if self._value < self.min or self._value >= self.max:
                raise ValueError("%s value %d doesn't match the range [%d;%d)!" % (self.name,
                                                                                   self._value,
                                                                                   self.min,
                                                                                   self.max))
        elif self.min is not None:
            if self._value < self.min:
                raise ValueError("%s value %d is less than minimum value %d!" % (self.name,
                                                                                 self._value,
                                                                                 self.min))
        elif self.max is not None:
            if self._value >= self.max:
                raise ValueError("%s value %d is greater than or equal maximum value %d!" % (self.name,
                                                                                             self._value,
                                                                                             self.max))


class ParameterGroup():
    """Group of parameters.

    Attributes:
      name: Name of the group.

    Use [] syntax for accessing parameter's values.
    par_a_value = par_group['par_a_name']
    """
    def __init__(self, name, params=[]):
        """Initialize parameter group.

        Args:
          params: Optional; List of the parameters to be stored inside the group.
        """
        self.name = name
        self._params = {}
        for p in params:
            self.add_param(p)

    def __str__(self):
        """Returns string representing group members and their values"""
        params = ['  ' + str(self._params[name]) for name in self._params.keys()]
        params_str = '\n'.join(params) if params else '  empty'
        return '%s:\n' % self.name + params_str

    def __getitem__(self, key):
        """To access parameter's value by it's name.

        Raises:
          KeyError: An error occured if parameter does not exists.
        """
        try:
            return self._params[key].value
        except KeyError:
            raise KeyError("Parameter with a name '%s' doesn't exist in a '%s' group!" % (key, self.name))

    def add_param(self, param):
        """Add parameter to the group"""
        self._params[param.name] = param


class Configuration():
    """ Collection of global parameters.

    Use [] syntax for accessing parameter's values.
    par_a_value = config['par_a_name']
    par_b_value = config['group_a_name']['par_b_name']
    """
    def __init__(self, params=[]):
        """Initialize parameter group.

        Args:
          params: Optional; List of the parameters to be stored inside the configuration.
            Note that this list is applied only after all built-in parameters will be created.
        """
        self._params = {}
        self._init_builtin_params()
        for p in params:
            self.add_param(p)

    def _init_builtin_params(self):
        """Initalize all built-in params"""

        # parameter read_filler
        self.add_param(Parameter(name='read_filler', value=0x0))

        # group address_calculation
        address_calculation_params = [
            Parameter(name='auto_increment_mode', value='none', allowlist=['none', 'data_width']),
            Parameter(name='auto_increment_value', value=4, min=1),
            Parameter(name='alignment_mode', value='data_width', allowlist=['none', 'data_width']),
            Parameter(name='alignment_value', value=4, min=1)
        ]
        self.add_param(ParameterGroup('address_calculation', address_calculation_params))

        # parameter register_reset
        self.add_param(Parameter(name='register_reset', value='sync_pos', allowlist=['sync_pos',
                                                                                     'sync_neg',
                                                                                     'async_pos',
                                                                                     'async_neg',
                                                                                     'init_only']))

        # group interface_generic
        interface_generic_params = [
            Parameter(name='type', value='lb', allowlist=['amm', 'apb', 'axil', 'lb']),
            Parameter(name='data_width', value='32'),
            Parameter(name='address_width', value='32'),
        ]
        self.add_param(ParameterGroup('interface_generic', interface_generic_params))

        # group interface_specific
        self.add_param(ParameterGroup('interface_specific'))

    def __str__(self):
        """Returns string representing all parameters and their values"""
        param_str = [str(self._params[name]) for name in self._params.keys()]
        return '\n'.join(param_str)

    def __getitem__(self, key):
        """To access parameter's value by it's name.

        Raises:
          KeyError: An error occured if parameter or group does not exists.
        """
        if isinstance(self._params[key], Parameter):
            try:
                return self._params[key].value
            except KeyError:
                raise KeyError("Parameter with a name '%s' doesn't exist in the configuration!" % key)
        else:
            try:
                return self._params[key]
            except KeyError:
                raise KeyError("Parameter group with a name '%s' doesn't exist in the configuration!" % key)

    def add_param(self, param):
        """Add parameter or group of parameters"""
        self._params[param.name] = param
