#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration module.
"""


class Parameter():
    """Generic parameter"""
    def __init__(self, name, value=None, allowlist=None, min=None, max=None):
        self.name = name
        self._value = value
        self._allowlist = allowlist
        self._min = min
        self._max = max
        if value is not None:
            self._check()

    def __str__(self):
        return '%s: %s' % (self.name, self.val)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._check()

    def _check(self):
        """Check parameter value correctness"""
        if self._allowlist is not None:
            if self._value not in self._allowlist:
                raise ValueError('%s parameter has no option %s in %s!' % (self.name,
                                                                           self._value,
                                                                           self._allowlist))
        elif (self._min is not None) and (self._max is not None):
            if self._value < self._min or self._value >= self._max:
                raise ValueError("%s value %d doesn't match the range [%d;%d)!" % (self.name,
                                                                                   self._value,
                                                                                   self._min,
                                                                                   self._max))
        elif self._min is not None:
            if self._value < self._min:
                raise ValueError("%s value %d is less than minimum value %d!" % (self.name,
                                                                                 self._value,
                                                                                 self._min))
        elif self._max is not None:
            if self._value >= self._max:
                raise ValueError("%s value %d is greater than or equal maximum value %d!" % (self.name,
                                                                                             self._value,
                                                                                             self._max))


class ParameterGroup():
    """Group of parameters"""
    def __init__(self, name):
        self.name = name
        self._params = {}

    def __str__(self):
        param_str = ['\t' + str(self._params[name]) for name in self._params.keys()]
        return '%s:\n' + '\n'.join(param_str)

    def __getitem__(self, key):
        return self._params[key].value

    def add_param(self, param):
        """Add parameter"""
        self._params[param.name] = param


class Configuration():
    """ Collection of global parameters """
    def __init__(self):
        self._params = {}

    def __str__(self):
        param_str = [str(self._params[name]) for name in self._params.keys()]
        return '\n'.join(param_str)

    def __getitem__(self, key):
        if isinstance(self._params[key], Parameter):
            return self._params[key].value
        else:
            return self._params[key]

    def add_param(self, param):
        """Add parameter or group of parameters"""
        self._params[param.name] = param
