# -*- mode:python; coding: utf-8 -*-

"""
Account
"""

from __future__ import absolute_import

__author__ = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from restfulie.client import Extend
from restfulie.cached import cached

# local submodule requirements
from ..api import SleipnirMapper


class Sleipnir(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend

    ACCOUNTS_API = {
        "me": {
            "endpoint": 'account/me',
            "method"  : 'get',
            "auth"    : 'sleipnir',
        },
        "update": {
            "endpoint": 'account/update',
            "method"  : 'patch',
            "flavor"  : 'application/json-patch',
            "auth"    : 'sleipnir',
            "body"    : True,
        },
        "update_avatar": {
            "endpoint": 'account/update/avatar',
            "method"  : 'put',
            "flavor"  : 'multipart',
            "auth"    : 'sleipnir',
            "compress": True,
            "required": ['avatar'],
        },
    }

    # pylint: disable-msg=C0103, E1101
    def me(self, callback):
        """Get own info"""
        return SleipnirMapper.BASE_API.invoke(
            self, self.ACCOUNTS_API["me"], None, {}, callback)

    @property
    @cached
    def accounts(self):
        """Get accounts related info"""
        return SleipnirMapper(self, self.ACCOUNTS_API, ignore=["me"])
