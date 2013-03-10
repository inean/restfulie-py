# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
persons
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

    PERSONS_API = {
      "search": {
        "endpoint" : '/persons/search',
        "method"   : 'get',
        "auth"     : "sleipnir",
        "required" : ['query'],
        },
      }

    @property
    @cached
    def persons(self):
        return SleipnirMapper(self, self.PERSONS_API)
