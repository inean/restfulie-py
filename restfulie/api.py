#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
BaseAPI
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.
from itertools import ifilter

__all__ = ['BaseAPI']

# Project requirements
from .restfulie import Restfulie


class BaseAPI(object):
    """
    Derive from here Custom API Implementations. All implementations
    MUST be stateless
    """

    API_BASE = None

    #pylint: disable-msg=W0613
    @classmethod
    def _get(cls, client, auth, endpoint, args, callback):
        """Implementation of verb GET"""
        return Restfulie.at(cls.API_BASE + endpoint) \
            .auth(client.credentials, method=auth)   \
            .get(callback=callback, params=args)

    @classmethod
    def _post(cls, client, endpoint, args, callback):
        """Implementation of verb POST"""
        raise NotImplementedError

    @classmethod
    def _upload(cls, client, source, args, callback=None):
        """Allow upload of files to server using POST verb"""
        raise NotImplementedError

    @classmethod
    def invoke(cls, client, call, args, callback=None):
        """Invoke method"""

        # check that requirements are passed
        path = call["endpoint"]
        requirements = call.get("required", ())
        for req in ifilter(lambda arg: arg not in args, requirements):
            err = "Missing arg '%s' for '%s'" % (req, path)
            raise AttributeError(err)

        # build endpoint
        endpoint = path % args
        auth     = call.get("auth")
        verb     = getattr(cls, "_" + call["method"])

        # remove used args
        path = call["endpoint"]
        func = lambda x: '%%(%s)' % x[0] not in path
        args = dict(ifilter(func, args.iteritems()))
                
        # invoke
        return verb(client, auth, endpoint, args, callback)

    @classmethod
    def query(cls, client, call, args, callback=None):
        """Implements RECOVER on a CRUD model"""
        return cls.invoke(client, call, args, callback)

        

