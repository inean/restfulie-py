# -*- mode:python; coding: utf-8 -*-

"""
users
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

    USERS_API = {
      "show": {
        "endpoint": '/users/show/%(username)s',
        "method"  : 'get',
        "required": ['username'],
        },
      "show_authorized": {
        "endpoint": '/users/show/%(username)s',
        "method"  : 'get',
        "auth"    : "sleipnir",
        "required": ['username'],
        },
      "update": {
          "endpoint": '/users/show/%(username)s',
          "method"  : 'patch',
          "auth"    : "sleipnir",
          "required": ['username', None],
      }
    }

    @property
    @cached
    def users(self):
        return SleipnirMapper(self, self.USERS_API)
