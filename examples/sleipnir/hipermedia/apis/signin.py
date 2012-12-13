
#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
users
"""

from __future__ import absolute_import

__author__   = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from restfulie.processor import auth_chain
from restfulie.client import Extend

# local submodule requirements
from ..api import API

# By default, we provide an url anf follow a normal flow, but we only
# require authenticate data, or check that user could operate, we use
# a shourcut chain, auth_chain to only get a valid set of tokens

class AuthAPI(API):
    CHAIN = auth_chain

class Sleipnir(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend

    SIGNIN_API = {
        "login" : {
            "endpoint" : '',
            "method"   : 'get',
            "auth"     : "sleipnir",
            #"secure"   : [True, None] # Use default port
        },
    }

    def signin(self, callback):
        return AuthAPI.invoke(self, self.SIGNIN_API["login"], {}, callback)
