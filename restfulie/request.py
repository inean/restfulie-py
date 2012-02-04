#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
request
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE file for details"

# Import here any required modules.

__all__ = ['Request']

# Project requirements
from .parser import Parser

class Request(object):
    """An HTTP request"""

    def __init__(self, config):
        self._config = config

    def __call__(self, callback=None, **payload):
        """
        Perform the request.The optional payload argument is sent to
        the server
        """
        env = {} if not payload else {'payload': kwargs}
        procs = list(self._config.processors)
        return Parser(procs).follow(callback, self._config, env)
