#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
users
"""

from __future__ import absolute_import

__author__   = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# local submodule requirements
from ..api import API
from ..client import Extend, validate


class Client(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend
  
    USERS_API = {
      "show" : {
        "endpoint" : 'users/show.json',
        "method"   : 'get',
        "auth"     : "twitter",
        "required" : ['screen_name'],
        },

      "timeline" : {
        "endpoint" : 'statuses/home_timeline.json',
        "method"   : 'get',
        "auth"     : "twitter",
        "required" : [],
        }
      }
    
    @validate('USERS_API')
    def users(self, action, args, callback):
        return API.query(self, self.USERS_API[action], args, callback)

    @validate('USERS_API')
    def timeline(self, action, args, callback):
        return API.query(self, self.USERS_API[action], args, callback)
    
