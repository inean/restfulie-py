#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
converter
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE file for details"

# Import here any required modules.

__all__ = ['Converters', 'ConverterMixin']

# Project requirements

# local submodule requirements

class ConverterError(Exception):
    """Resource exception"""

class Converters(object):
    """Utility methods for converters."""

    types = {}

    @staticmethod
    def register(a_type, converter):
        """Register a converter for the given type"""
        Converters.types[a_type] = converter

    @staticmethod
    def marshaller_for(a_type):
        """Return a converter for the given type"""
        if type(a_type) in (str, unicode,):
            # common case. Throw a key error exception if no valid one
            # has been registered"
            if ";" not in a_type:
                return Converters.types[a_type]
            # Passed a composed string (';' separated)
            a_type, key = a_type.split(";"), a_type
        else:
            # Passed a list
            assert len(a_type) > 0
            a_type, key = a_type, ";".join(a_type)

        # Dinamically, create a valid converter if required for this
        # kind of element.Converters are stateless,
        return Converters.types.setdefault(   \
            key,                              \
            Converters.types[a_type[0]].__class__(a_type[1:]))


class MetaConverter(type):
    """Converter Metaclass"""

    def __init__(mcs, name, bases, dct):
        type.__init__(mcs, name, bases, dct)
        if name.endswith("Converter"):
            for a_type in mcs.types:
                Converters.register(a_type, mcs())


class ConverterMixin(object):
    """
    Abstract class to define converter classes. This class has support
    to create chained converters
    """

    __metaclass__ = MetaConverter

    def __init__(self, a_type_list=None):
        # Store next converter in chain
        self._chain = None
        assert not a_type_list or hasattr('__iter__', a_type_list)
        # Allow this class to also be used like a dead end
        if a_type_list and len(a_type_list) > 1:
            self.chain = Converters.marshaller_for(list(a_type_list)[1:])

    def marshal(self, content):
        """Does nothing"""
        return content if not self.chain else self.chain.marshal(content)

    def unmarshal(self, content):
        """Returns content without modification"""
        return content if not self.chain else self.chain.marshal(content)

            
class PlainConverter(ConverterMixin):
    """Dummy converter to plain text"""

    types = ['text/plain']

    def __init__(self):
        ConverterMixin.__init__(self)
