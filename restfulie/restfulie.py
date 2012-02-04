#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
Request
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE file for details"

# Import here any required modules.

__all__ = ['Response']

# Project requirements
from .configuration import Configuration

#pylint: disable-msg=R0903
class Restfulie(object):
    """Restfulie entry point"""

    # pylint: disable-msg=C0103
    @staticmethod
    def at(uri):
        """Create a new entry point for executing requests"""
        return Configuration(uri)
