# -*- mode:python; coding: utf-8 -*-

"""
Persons
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

    PERSONS_API = {
        "search": {
            "endpoint": 'persons/search',
            "method"  : 'get',
            "auth"    : "sleipnir",
            "required": ['query'],
        },
    }

    @property
    @cached
    def persons(self):
        """Accessor to persons api"""
        return SleipnirMapper(self, self.PERSONS_API)
