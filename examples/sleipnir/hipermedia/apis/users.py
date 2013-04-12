# -*- mode:python; coding: utf-8 -*-

"""
Users
"""

from __future__ import absolute_import

__author__ = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from restfulie.client import Extend
from restfulie.cached import cached

# local submodule requirements
from ..api import SleipnirMapper


# pylint: disable-msg=R0903
class Sleipnir(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend

    USERS_API = {
        "show": {
            "endpoint": 'users/show/%(username)s',
            "method"  : 'get',
            "required": ['username'],
        },
        "show_authorized": {
            "endpoint": 'users/show/%(username)s',
            "method"  : 'get',
            "auth"    : "sleipnir",
            "required": ['username'],
        },
        "update": {
            "endpoint": 'users/show/%(username)s',
            "method"  : 'patch',
            "auth"    : "sleipnir",
            "required": ['username', None],
        }
    }

    @property
    @cached
    def users(self):
        """Accesor to users API"""
        return SleipnirMapper(self, self.USERS_API)
