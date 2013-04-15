# -*- mode:python; coding: utf-8 -*-

"""
API
"""

from __future__ import absolute_import

__author__ = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any common modules

__all__ = ['SleipnirMapper', 'SleipnirAuth']

# Import here local required modules
from restfulie.api import BaseAPI, BaseMapper
from restfulie.auth import OAuthMixin
from restfulie.client import Client
from restfulie.processor import auth_chain


#pylint: disable-msg=W0232, R0903
class Sleipnir(Client):
    """Base client class for Sleipnir API"""

    # When scaling, it's probably a good idea to split oauth and api
    # servers. Services is read at Startup. Services is read at Client
    # startup to register safe values for well known services. Use
    # settings to override this with a more accurate ones
    SERVICES = {
        'sleipnir/api1': {
            'protocol': 'http',
            'host': 'api.sleipnir-project.com',
            'path': '/1',
            'port': 80,
            'secure_port': 443,
            'ca_certs': None,
            'enforce': False,
        },
        'sleipnir/oauth1': {
            'protocol': 'https',
            'host': 'api.sleipnir-project.com',
            'path': '/oauth',
            'port': 80,
            'secure_port': 443,
            'ca_certs': None,
            'enforce': False,
        },
    }

    # Service Map. It allow us to add a level of indirection to
    # diverge between functionality (target key), and WHO provides
    # that functionality
    ENDPOINTS = {
        'sleipnir': {
            'apiv1': 'sleipnir/api1',
            'oauth': 'sleipnir/oauth1',
        },
    }


#pylint: disable-msg=W0223, R0903
class SleipnirAuth(OAuthMixin):
    """ oauth method """

    # Base Url. OAuthMixin use target directly to resolve agaist
    # Services singleton. We delegate service registration to Client
    # (Sleipnir) object, in this case
    ENDPOINT = "sleipnir/oauth"

    # Auth mechanism implemented
    implements = "sleipnir"


# pylint: disable-msg=R0903
class SleipnirMapper(BaseMapper):
    """Mapper to make rest invokations more pythonic"""

    # pylint: disable-msg=R0903
    class SleipnirAPI(BaseAPI):
        """Extend BaseAPI class with custom values"""

        # Base Url. In this case we use
        ENDPOINT = "sleipnir/apiv1"

        # Our api is json based only
        FLAVORS = ["json"]

        # define default timeouts
        CONNECT_TIMEOUT = 5
        REQUEST_TIMEOUT = 10

    # pylint: disable-msg=R0903
    class SleipnirAuthAPI(SleipnirAPI):
        """Extense SleipnirAPI to sort chain on auth flows"""

        # Base Url. In this case we use oauth to enforce security on
        # handshake
        ENDPOINT = "sleipnir/oauth"

        CHAIN = auth_chain

    # Register defined classes
    BASE_API = SleipnirAPI
    AUTH_API = SleipnirAuthAPI
