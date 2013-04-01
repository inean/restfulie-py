# -*- mode:python; coding: utf-8 -*-

"""
Client
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.
from contextlib import contextmanager

__all__ = ['Client', 'Extend']

# local submodule requirements
from .credentials import Credentials


class Extend(type):
    """
    Allow Ad-hoc inheritance. See
    http://code.activestate.com/recipes/412717-extending-classes/ for
    details
    """

    clients = {}

    #pylint: disable-msg=W0613
    def __new__(mcs, name, bases, dct):
        prev = Extend.clients[name]
        del dct['__module__']
        del dct['__metaclass__']
        for key, value in dct.iteritems():
            if key == "__doc__":
                continue
            setattr(prev, key, value)
        return prev


class ClientMeta(type):
    """
    Simple metaclass to make client subclasses discoverable by
    Extend metaclass
    """
    def __init__(cls, name, bases, dct):
        super(ClientMeta, cls).__init__(name, bases, dct)
        assert name not in Extend.clients
        Extend.clients[name] = cls


class Client(object):
    """Base class to implement a remote API"""

    __metaclass__ = ClientMeta

    # Allow to translate a Target variable into a valid service tag
    # already registered in session singleton instance
    TARGETS = {}

    def __init__(self, credentials=None):
        self._config = credentials or Credentials()

    @contextmanager
    def configure(self):
        """Get an accessor to credentials element"""
        yield self._config

    @property
    def credentials(self):
        """Get credentials element"""
        return self._config
