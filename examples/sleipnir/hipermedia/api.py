# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
API
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any common modules
import urlparse
import itertools

__all__ = ['SleipnirMapper', 'SleipnirAuth']

# Import here local required modules
from restfulie.api       import BaseAPI, BaseMapper
from restfulie.auth      import OAuthMixin
from restfulie.client    import Client
from restfulie.processor import auth_chain


#pylint: disable-msg=W0232
class Sleipnir(Client):
    """Base client class for Sleipnir API"""

    # When scaling, it's probably a good idea to split oauth and api
    # servers
    URLS = {
        'apiv1':  "http://api.sleipnir-project.com/1",
        'oauth': "https://api.sleipnir-project.com/oauth",
    }

    @classmethod
    def override_server(cls, url, override_api=True, override_oauth=True):
        """
        Use this class method to set sanity values for class
        properties when a custom server must be used
        """
        # Parse url; pylint:disable-msg=W0212,E1101
        url = urlparse.urlparse(url)
        assert url.netloc and url.scheme
        url = dict(itertools.izip(url._fields, url))

        # Override class urls
        if override_api:
            url['path'] = "/1"
            cls.URLS['apiv1'] = urlparse.urlunparse(url)
        if override_oauth:
            url['path'] = "/oauth"
            cls.URLS['oauth'] = urlparse.urlunparse(url)


#pylint: disable-msg=W0223
class SleipnirAuth(OAuthMixin):
    """ oauth method """

    # Decide wich class will be using this api. Base Url will be
    # fetched from them
    CLIENT = Sleipnir

    # Auth mechanism implementd
    implements = "sleipnir"


class SleipnirMapper(BaseMapper):
    """Mapper to make rest invokations more pythonic"""

    class SleipnirAPI(BaseAPI):
        """Extend BaseAPI class with custom values"""

        # Decide wich class will be using this api. Base Url will be
        # fetched from them
        CLIENT  = Sleipnir

        # Base Url
        TARGET  = "apiv1"

        # Our api is json based only
        FLAVORS = ["json"]

        # define default timeouts
        CONNECT_TIMEOUT = 5
        REQUEST_TIMEOUT = 10

    class SleipnirAuthAPI(SleipnirAPI):
        CHAIN = auth_chain

        # Override Target to focus on oauth ones
        TARGET = "oauth"

    # Register defined classes
    BASE_API = SleipnirAPI
    AUTH_API = SleipnirAuthAPI
