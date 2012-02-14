#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
API
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

__all__ = ['API']

from restfulie.api import BaseAPI

class API(BaseAPI):
    """Extend BaseAPI class with custom methods"""

    API_BASE = "http://api.tweeter.com/1"
