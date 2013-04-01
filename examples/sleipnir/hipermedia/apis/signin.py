# -*- mode:python; coding: utf-8 -*-

"""
Sigin
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from restfulie.client import Extend

# local submodule requirements
from ..api import SleipnirMapper

# By default, we provide an url anf follow a normal flow, but we only
# require authenticate data, or check that user could operate, we use
# a shourcut chain, auth_chain to only get a valid set of tokens


class Sleipnir(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend

    SIGNIN_API = {
        "login": {
            "auth"  : "sleipnir",
            "method": 'get',
            # Force secure connection. Use default port.
            "secure": [True, None],
        },
    }

    def signin(self, callback):
        return SleipnirMapper.AUTH_API.invoke(
            self, self.SIGNIN_API["login"], None, {}, callback)
