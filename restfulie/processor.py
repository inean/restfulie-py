#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
processors
"""

from __future__ import absolute_import

__autor__ = "caelum - http://caelum.com.br"
__modified_by__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.

__all__ = ['Configuration']

# Project requirements
from base64 import encodestring
from copy import copy
from tornado.httpclient import HTTPClient, AsyncHTTPClient

# local submodule requirements
from .converters import Converters
from .response import Response
from .request import Request

__all__ = [
    'AuthenticationProcessor',
    'ExecuteRequestProcessor',
    'PayloadMarshallingProcessor',
    'RedirectProcessor',
    ]

#pylint: disable-msg=R0903
class RequestProcessor(object):
    """Base class for all processors"""

    def execute(self, callback, chain, request, env):
        """Command called to be runned"""
        raise NotImplementedError('Subclasses must implement this method')


#pylint: disable-msg=R0903, R0922
class AuthenticationProcessor(RequestProcessor):
    """Abstract class for authentication methods"""

    USERNAME, PASSWORD, METHOD = xrange(0, 3)

    implements = None

    def execute(self, callback, chain, request, env):
        credentials = request.credentials
        if credentials and credentials[self.METHOD] == self.implements:
            request.headers['authorization'] = self._encode(request.credentials)
        return chain.follow(callback, request, env)

    def _encode(self, credentials):
        """Return authentication header value"""
        raise NotImplementedError


#pylint: disable-msg=R0903
class AuthenticationSimpleProcessor(AuthenticationProcessor):
    """Processor responsible for making HTTP simple auth"""

    implements = "simple"

    def _encode(self, credentials):
        username, password, _ = credentials
        return "Basic %s" % encodestring("%s:%s" % (username, password))[:-1]


class ExecuteRequestProcessor(RequestProcessor):
    """
    Processor responsible for getting the body from environment and
    making a request with it.
    """
    @staticmethod
    def _sync(request, env):
        """Run blocked"""
        response = HTTPClient().fetch(
            request.uri,
            method=request.verb,
            body=env.get("body"), 
            headers=request.headers)
        return Response(response)

    @staticmethod
    def _async(callback, request, env):
        """Run async"""
        AsyncHTTPClient().fetch(
            request.uri,
            lambda x: callback(Response(x)),
            method=request.verb,
            body=env.get("body"), 
            headers=request.headers)
        return None

    def execute(self, callback, chain, request, env):
        return self._sync(request, env) \
            if not callable(callback)          \
            else self._async(callback, request, env)


class PayloadMarshallingProcessor(RequestProcessor):
    """Responsible for marshalling the payload in environment"""

    def execute(self, callback, chain, request, env):
        if "payload" in env:
            content_type = request.headers.get("content-type")
            marshaller   = Converters.marshaller_for(content_type)
            env["body"]  = marshaller.marshal(env["payload"])
            del(env["payload"])
        return chain.follow(callback, request, env)


class RedirectProcessor(RequestProcessor):
    """
    A processor responsible for redirecting a client to another URI
    when the server returns the location header and a response code
    related to redirecting.
    """
    REDIRECT_CODES = ['201', '301', '302']

    def _redirect(self, result):
        """Get redirection url, if any"""
        return result.headers.get("location") \
            if (result.code in self.REDIRECT_CODES) else None

    def execute(self, callback, chain, request, env):
        def _on_resource(resource):
            """resource callback"""
            assert callable(callback)
            # copy configuration and update url
            url = self._redirect(resource)
            if not url:
                return callback(resource)
            # make a new request
            config = copy(request.config)
            config.url = url
            return Request(self)(callback)
        # chain
        return chain.follow(_on_resource, request, env)    \
            if callable(callback) else chain.follow(callback, request, env)


# Main tornado chain (Use follow_redirects so RedirectProcessor is not
# required anymore

#pylint:disable-msg=C0103
tornado_chain = [
    AuthenticationSimpleProcessor(),
#    RedirectProcessor(),
    PayloadMarshallingProcessor(),
    ExecuteRequestProcessor(),
    ]
