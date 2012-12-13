#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
API
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

__all__ = ['API']

from restfulie.api    import BaseAPI, BaseMapper
from restfulie.auth   import OAuthMixin
from restfulie.client import Client

class Twitter(Client):
    """Base client class for Sleipnir API"""

#pylint: disable-msg=W0223         
class TwitterAuth(OAuthMixin):
    """ oauth method """
    
    implements = "twitter"

    @property
    def request_url(self):
        return "https://api.twitter.com/oauth/request_token"

    @property
    def authorize_url(self):
        return "https://api.twitter.com/oauth/authorize"

    @property
    def access_url(self):
        return "https://api.twitter.com/oauth/access_token"
        

class API(BaseAPI):
    """Extend BaseAPI class with custom methods"""

    # default api address
    API_BASE = "https://api.twitter.com/1"

    # Our api is json based only
    FLAVORS  = ["json"]

    # define default timeouts
    CONNECT_TIMEOUT = 5
    REQUEST_TIMEOUT = 10

class APIMapper(BaseMapper):
    """Mapper to make rest invokations more pythonic"""
    BASE_API = API