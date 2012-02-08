#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
API
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.
from itertools import ifilter

__all__ = ['API']

# Project requirements
from .restfulie import Restfulie

class API(object):
    """
    Derive from here Custom API Implementations. All implementations
    MUST be stateless
    """

    API_BASE = 'http://api.twitpic.com/2/'

    #pylint: disable-msg=W0613
    @classmethod
    def _get(cls, client, endpoint, args):
        """Implementation of verb GET"""
        return Restfulie.at(cls.API_BASE + endpoint).get(params=args)

    @classmethod
    def _post(cls, client, endpoint, args):
        """Implementation of verb POST"""
        raise NotImplementedError

    @classmethod
    def query(cls, client, call, args):
        """Implements RECOVER on a CRUD model"""
        # validate info
        for req in ifilter(lambda x: x not in call["required"], args):
            error = "Missing arg '%s' for '%s" % (req, call["endpoint"])
            raise AttributeError(error)
        # invoke
        verb = getattr(cls, "_" + call["method"])
        return verb(client, call["endpoint"], args)

    @classmethod
    def upload(cls, client, source, args):
        """Allow upload of files to server"""
        raise NotImplementedError

