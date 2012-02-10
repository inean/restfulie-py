#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
configuration
"""

from __future__ import absolute_import

__author__ = "caelum - http://caelum.com.br"
__modified_by__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.
import re

__all__ = ['Configuration']

# Project requirements
from tornado.httputil import HTTPHeaders

# local submodule requirements
from .processor import tornado_chain
from .request import Request


class Configuration(object):
    """Configuration object for requests at a given URI"""

    HTTP_VERBS = [
        'delete',
        'get',
        'head',
        'options',
        'patch',
        'post',
        'put',
        'trace'
        ]

    FLAVORS = {
        'json': {
            'content-type': 'application/json',
            'accept':       'application/json'
            },
        'xml': {
            'content-type': 'application/xml',
            'accept':       'application/xml'
            },
        'plain': {
            'content-type': 'text/plain',
            'accept':       'text/plain',
            },
        }

    def __init__(self, uri, flavors=None, chain=None):
        """Initialize the configuration for requests at the given URI"""
        self.uri         = uri
        self.headers     = HTTPHeaders()
        self.flavors     = flavors or ['json', 'xml']
        self.processors  = chain or tornado_chain
        self.credentials = []
        self.verb        = None

    def __getattr__(self, value):
        """
        Perform an HTTP request. This method supports calls to the following
        methods: delete, get, head, options, patch, post, put, trace

        Once the HTTP call is performed, a response is returned (unless the
        async method is used).
        """
        if (value not in self.HTTP_VERBS):
            raise AttributeError(value)

        # store current verb to be passed to Request
        self.verb = value.upper()

        # set accept if it wasn't set previously
        if 'accept' not in self.headers:
            for flavor in self.flavors:
                self.headers.add('accept', self.FLAVORS[flavor]['accept'])
        return Request(self)

    def use(self, feature):
        """Register a feature (processor) at this configuration"""
        self.processors.insert(0, feature)
        return self

    def as_(self, content_type):
        """Set up the Content-Type"""
        assert content_type
        self.headers["accept"] = content_type
        self.headers["content-type"] = content_type
        return self

    def accepts(self, content_type):
        """Configure the accepted response format"""
        self.headers['accept'] = content_type + ', ' + self.headers['accept'] \
            if 'accept' in self.headers else content_type
        return self

    def auth(self, credentials, path="*", method='plain'):
        """Authentication feature. It does simple HTTP auth"""

        # process a regex valid for path
        rmatch = re.compile("%s$" % path)  if not path.endswith('*') \
            else re.compile("%s.*" % path.rsplit('*', 1)[0])

        # credentials must be a callable, but allow to pass an object
        # instance or something with attributes
        if not callable(credentials):
            credentials = lambda: credentials

        # not store it
        self.credentials.append((rmatch, method, credentials))
        return self
