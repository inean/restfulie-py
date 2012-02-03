#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
resource

Represents a generic gateway to AMQP implementation
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE file for details"

# Import here any required modules.

__all__ = ['Resource']

# Project requirements

# local submodule requirements

class ResourceError(Exception):
    """Resource exception"""

#pylint: disable-msg=R0921
class Resource(object):
    """Prepares a connection. only get a pika connection is lazy created"""

    def links(self):
        """Returns a list of all links."""
        raise NotImplementedError

    def link(self, rel):
        """Return a Link with rel."""
        raise NotImplementedError


