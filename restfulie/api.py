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

# Create:
#-------.
# PUT:  if you are sending the full content of the specified resource (URL).
# POST: if you are sending a command to the server to create a
#       subordinate of the specified resource, using some server-side
#       algorithm.

# Retrieve
# --------
# GET

# Update
# -------
# PUT:   if you are updating the full content of the specified resource.
# PATCH: if you are requesting the server to update one or
#        more subordinates of the specified resource.

# Delete
# ------
# DELETE.

class BaseAPI(object):
    """
    Derive from here Custom API Implementations. All implementations
    MUST be stateless
    """

    API_BASE = None
    FLAVORS  = None
    CHAIN    = None

    # Timeouts
    CONNECT_TIMEOUT = None
    REQUEST_TIMEOUT = None
    
    
    #pylint: disable-msg=W0613
    @classmethod
    def _get(cls, client, auth, endpoint, flavor, args, callback):
        """Implementation of verb GET"""
        return Restfulie.at(cls.API_BASE + endpoint, cls.FLAVORS, cls.CHAIN) \
            .auth(client.credentials, method=auth)                           \
            .accepts(flavor)                                                 \
            .until(cls.REQUEST_TIMEOUT, cls.CONNECT_TIMEOUT)                 \
            .get(callback=callback, params=args)

    @classmethod
    def _post(cls, client, auth, endpoint, flavor, args, callback):
        """Implementation of verb POST"""

        #default to form-urlencode. If somthing that smells like a
        #file (has read function) is pased in args, encode it as
        #multipart form

        if any((hasattr(arg, "read") for arg in args.itervalues())):
            flavor = "multipart"
            
        return Restfulie.at(cls.API_BASE + endpoint, cls.FLAVORS, cls.CHAIN) \
            .as_(flavor)                                                     \
            .auth(client.credentials, method=auth)                           \
            .until(cls.REQUEST_TIMEOUT, cls.CONNECT_TIMEOUT)                 \
            .post(callback=callback, **args)

    @classmethod
    def _put(cls, client, auth, endpoint, flavor, args, callback):
        """Implementation of verb PUT"""

        #default to form-urlencode. If somthing that smells like a
        #file (has read function) is pased in args, encode it as
        #multipart form

        if any((hasattr(arg, "read") for arg in args.itervalues())):
            flavor = "multipart"
            
        return Restfulie.at(cls.API_BASE + endpoint, cls.FLAVORS, cls.CHAIN) \
            .as_(flavor)                                                     \
            .auth(client.credentials, method=auth)                           \
            .until(cls.REQUEST_TIMEOUT, cls.CONNECT_TIMEOUT)                 \
            .put(callback=callback, **args)

    @classmethod
    def _patch(cls, client, auth, endpoint, flavor, args, callback):
        """Implementation of verb PATCH"""

        # JSON path expexts an array of objects. Internally, We need
        # to pass Request object will asumme that we are providing an
        # array if args is defined as a length 1 dict with None as key
        # See also:
        # https://datatracker.ietf.org/doc/draft-ietf-appsawg-json-patch/
            
        return Restfulie.at(cls.API_BASE + endpoint, cls.FLAVORS, cls.CHAIN) \
            .as_(flavor)                                                     \
            .auth(client.credentials, method=auth)                           \
            .until(cls.REQUEST_TIMEOUT, cls.CONNECT_TIMEOUT)                 \
            .patch(callback=callback, **args)

    @classmethod
    def _delete(cls, client, auth, endpoint, flavor, args, callback):
        """Implementation of verb DELETE"""
        return Restfulie.at(cls.API_BASE + endpoint, cls.FLAVORS, cls.CHAIN) \
            .auth(client.credentials, method=auth)                           \
            .accepts(flavor)                                                 \
            .until(cls.REQUEST_TIMEOUT, cls.CONNECT_TIMEOUT)                 \
            .get(callback=callback, params=args)

        
    @classmethod
    def invoke(cls, client, call, args, callback=None):
        """Invoke method"""

        # check that requirements are passed
        path = call["endpoint"]
        flavor = call.get("flavor")
        requirements = call.get("required", ())
        for req in ifilter(lambda arg: arg not in args, requirements):
            err = "Missing arg '%s' for '%s'" % (req, path)
            raise AttributeError(err)

        # build endpoint
        endpoint = path % args
        auth     = call.get("auth")
        verb     = getattr(cls, "_" + call["method"])

        # remove used args
        func = lambda x: '%%(%s)' % x[0] not in path
        args = dict(ifilter(func, args.iteritems()))
                
        # invoke
        return verb(client, auth, endpoint, flavor, args, callback)

        

