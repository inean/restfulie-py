#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
credentials
"""

from __future__ import absolute_import

__author__   = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.

__all__ = ['Credentials']


class Credentials(object):
    """
    Base class to define required credentials to use a remote
    service
    """

    def __init__(self):
        self._api_key         = None
        self._consumer_key    = None
        self._consumer_secret = None

    @property
    def api_key(self):
        """Get API key required to use remote service"""
        return self._api_key or ""

    @api_key.setter
    def api_key(self, value):
        """Set API key requires to use remote service"""
        self._api_key = value

    @property
    def consumer_key(self):
        """Get required key to authenticate (login)"""
        return self._consumer_key or ""

    @consumer_key.setter
    def consumer_key(self, value):
        """Set auth key"""
        self._consumer_key = value

    @property
    def consumer_secret(self):
        """Get password"""
        return self._consumer_secret or ""

    @consumer_secret.setter
    def consumer_secret(self, value):
        """Set password"""
        self._consumer_secret = value

