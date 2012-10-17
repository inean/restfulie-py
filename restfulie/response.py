#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
request
"""

from __future__ import absolute_import

__author__ = "caelum - http://caelum.com.br"
__modified_by__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.

__all__ = ['Response']

# Project requirements
from .converters import Converters
from .links import Links


class Response(object):
    """Handle and parse a HTTP response"""

    def __init__(self, response):
        self._response = response
        self._resource = None

    def __getattr__(self, key):
        return self.resource[key]

    def __contains__(self, key):
        return key in self.resource
        
    @property
    def headers(self):
        """Returns HTTP headers"""
        return self._response.headers

    @property
    def code(self):
        """Returns response code"""
        return self._response.code

    @property
    def body(self):
        """Returns a formatted body"""
        return self._response.body

    @property
    def resource(self):
        """Unmarshalled object of the response body"""
        if not self._resource:
            content_type = self._response.headers.get_list('content-type')[0]
            converter = Converters.marshaller_for(content_type.split(';')[0])
            self._resource = converter.unmarshal(self._response.buffer)
        return self._resource
    
    @property
    def links(self):
        """Returns the Links of the header"""
        if not hasattr(self, '_links'):
            self._links = self.resource.links()
            values = self._response.headers.get('link')
            self._links.update([link for link in Links.parse(values)])
        return self._links

    def link(self, rel):
        """Get a link with 'rel' from header"""
        return self.links.rel

    @property
    def error(self):
        if not hasattr(self, '_error'):
            self._error = self.resource.error()
        return self._error
        
