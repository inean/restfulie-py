#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
parser
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE file for details"

# Import here any required modules.

__all__ = ['Parser']


#pylint: disable-msg=R0903
class Parser(object):
    """Executes processors ordered by the list"""

    def __init__(self, processors):
        self._processors = processors

    def follow(self, callback, request, env=None):
        """Follow chain"""
        processor = self._processors.pop(0)
        return processor.execute(callback, self, request, env or {})
