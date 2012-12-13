#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
users
"""

from __future__ import absolute_import

__author__   = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import required modules
from restfulie.client import Extend

# local submodule requirements
from ..api import API, APIMapper


class Twitter(object):
    """This class will extend main Client object"""

    __metaclass__ = Extend
  
    USERS_API = {
      "show" : {
        "endpoint" : '/users/show.json',
        "method"   : 'get',
        "auth"     : 'twitter',
        "required" : ['screen_name'],
        },

      "timeline" : {
        "endpoint" : '/statuses/home_timeline.json',
        "method"   : 'get',
        "auth"     : 'twitter',
        }
      }
    
    def timeline(self, callback):
        return API.invoke(self, self.USERS_API["timeline"], None, {}, callback)

    @property
    def users(self):
        return APIMapper(self, self.USERS_API, ignore=["timeline"])
    
