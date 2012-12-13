
#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
persons
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

    PERSONS_API = {
      "search" : {
        "endpoint" : '/persons/search',
        "method"   : 'get',
        "auth"     : "sleipnir",
        "required" : ['query'],
        },
      }

    @property
    @cached
    def persons(self):
        return APIMapper(self, self.PERSONS_API)
