# -*- mode:python; coding: utf-8 -*-

"""
Account
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from restfulie.client import Extend

# local submodule requirements
from ..api import SleipnirMapper

# Optional dependences
try:
    from sleipnir.core.decorators import cached
except ImportError:
    from functools import wraps

    def cached(func):
        @wraps(func)
        def wrapper(*args, **kwds):
            return func(*args, **kwds)
        return wrapper


class Sleipnir(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend

    ACCOUNTS_API = {
        "me": {
            "endpoint": '/account/me',
            "method"  : 'get',
            "auth"    : 'sleipnir',
        },
        "update": {
            "endpoint": '/account/update',
            "method"  : 'patch',
            "flavor"  : 'application/json-patch',
            "auth"    : 'sleipnir',
            "body"    : True,
        },
        "update_avatar": {
            "endpoint": '/account/update/avatar',
            "method"  : 'put',
            "flavor"  : 'multipart',
            "auth"    : 'sleipnir',
            "compress": True,
            "required": ['avatar'],
        },
    }

    def me(self, callback):
        return SleipnirMapper.BASE_API.invoke(
            self, self.ACCOUNTS_API["me"], None, {}, callback)

    @property
    @cached
    def accounts(self):
        return SleipnirMapper(self, self.ACCOUNTS_API, ignore=["me"])
