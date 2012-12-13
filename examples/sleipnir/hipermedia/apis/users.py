
#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
users
"""

from __future__ import absolute_import

__author__   = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from sleipnir.core.decorators import cached
from restfulie.client import Extend

# local submodule requirements
from ..api import API, APIMapper


class Sleipnir(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend
  
    USERS_API = {
      "show" : {
        "endpoint" : '/users/show/%(username)s',
        "method"   : 'get',
        "required" : ['username'],
        },

      "show_authorized" : {
        "endpoint" : '/users/show/%(username)s',
        "method"   : 'get',
        "auth"     : "sleipnir",
        "required" : ['username'],
        },
        
      "update": {
          "endpoint" : '/users/show/%(username)s',
          "method"   : 'patch',
          "auth"     : "sleipnir",
          "required" : ['username', None],
      }
    }
    
    @property
    @cached
    def users(self):
        return APIMapper(self, self.USERS_API)
