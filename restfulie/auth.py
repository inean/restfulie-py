#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
processors
"""

from __future__ import absolute_import

__author__ = "caelum - http://caelum.com.br"
__modified_by__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.
from base64 import b64encode
from urllib import splittype, splithost

__all__ = []

# Project requirements
from oauth2 import Request, SignatureMethod_HMAC_SHA1

try:
    from urlparse import parse_qs
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs


# local submodule requirements
from .processor import AuthMixin


#pylint: disable-msg=R0903
class BasicAuth(AuthMixin):
    """Processor responsible for making HTTP simple auth"""

    implements = "plain"

    def authorize(self, credentials, request, env):
        encode = b64encode("%s:%s" % credentials())
        request.headers['authorization'] = 'Basic %s' %  encode


class OAuth(AuthMixin):
    """ oauth method """

    implements = "oauth"

    DEFAULT_POST_CONTENT_TYPE = 'application/x-www-form-urlencoded'

    @staticmethod
    def validate_consumer(consumer):
        """ validate a consumer agains oauth2.Consumer object """
        if not hasattr(consumer, "key"):
            raise ValueError("Invalid consumer.")
        return consumer

    @staticmethod
    def validate_token(token):
        """ validate a token agains oauth2.Token object """
        if token is not None and not hasattr(token, "key"):
            raise ValueError("Invalid token.")
        return token

    def authorize(self, credentials, request, env):
        consumer, token, method = credentials()

        # validate params
        consumer = self.validate_consumer(consumer)
        token    = self.validate_token(token)
        method   = method or SignatureMethod_HMAC_SHA1()

        # post ?
        headers  = request.headers
        if request.verb == "POST":
            ctype = headers.get('content-type', self.DEFAULT_POST_CONTENT_TYPE)
            headers['content-type'] = ctype
        isform = headers.get('content-type') == self.DEFAULT_POST_CONTENT_TYPE

        # process post contents if required
        body, parameters = env.get('body', ''), None
        if isform and body:
            parameters = parse_qs(body)

        # process token
        req = Request.from_consumer_and_token(          \
            consumer, token, request.verb, request.uri, \
            parameters, body, isform)
        req.sign_request(method, consumer, token)

        # calculate realm
        schema, rest = splittype(request.uri)
        hierpart = ''
        if rest.startswith('//'):
            hierpart = '//'
        host, rest = splithost(rest)
        realm = schema + ':' + hierpart + host

        # process body if form or uri if a get/head
        if isform:
            env['body'] = req.to_postdata()
        elif request.verb in ('GET', 'HEAD',):
            request.uri = req.to_url()
        else:
            headers.update(req.to_header(realm=realm))
