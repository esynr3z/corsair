#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Enumerated value for bit field
"""

from . import utils
from . import config


class EnumValue():
    """Enumerated value.

    :param name: Enum name
    :type name: str
    :param value: Enum value
    :type value: int
    :param description: Enum description
    :type description: str
    """

    def __init__(self, name='enum', value=0, description='Enumerated value', **args):
        self.name = name
        self.description = description
        self.value = value
        self.etc = args

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise TypeError("Failed to compare '%s' with '%s'!" %
                            (repr(self), repr(other)))
        else:
            return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        if self.__class__ != other.__class__:
            raise TypeError("Failed to compare '%s' with '%s'!" %
                            (repr(self), repr(other)))
        else:
            return not self.__eq__(other)

    def __repr__(self):
        return 'EnumValue(%s)' % repr(self.name)

    def __str__(self):
        return self.as_str()

    def as_str(self, indent=''):
        """Create an indented string with the enum information."""
        enum_str = indent + \
            '%s: %d - %s' % (self.name, self.value, self.description)
        return enum_str

    def as_dict(self):
        """Create a dictionary with the key attributes of the bit field."""
        d = {'name': self.name, 'description': self.description, 'value': self.value}
        d.update(self.etc)
        return d

    @property
    def name(self):
        """Name of the enum."""
        return utils.force_name_case(self._name)

    @name.setter
    def name(self, value):
        if not utils.is_str(value):
            raise ValueError(
                "'name' attribute has to be 'str', but '%s' provided for the enum!" % type(value))
        self._name = value

    @property
    def value(self):
        """Value of the enum."""
        return self._value

    @value.setter
    def value(self, value_):
        self._value = utils.str2int(value_)

    @property
    def description(self):
        """Description of the enum."""
        return self._description

    @description.setter
    def description(self, value):
        if not utils.is_str(value):
            raise ValueError("'description' attribute has to be 'str', but '%s' provided for the '%s' enum!" %
                             (type(value), self.name))
        self._description = value

    def validate(self):
        """Validate parameters of the enum."""
        # value type
        assert utils.is_non_neg_int(self.value), \
            "Enum value '%s' for '%s' enum is wrong! Only non-negative integers are allowed." % \
            (self.value, self.name)
