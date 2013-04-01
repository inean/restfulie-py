# -*- mode:python; coding: utf-8 -*-

"""
Services
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"


# pylint: disable-msg=R0903
class Services(object):
    """
    Services configuration class. Provides information about available
    services location and security requirements
    """

    URLS = {
        'sleipnir-apiv1': "http://api.sleipnir-project.com/1",
        'sleipnir-oauth': "https://api.sleipnir-project.com/oauth",
    }
    CACERTS = {
        'sleipnir-apiv1': None,
        'sleipnir-oauth': None,
    }

    @classmethod
    def get_instance(cls):
        """Get service singleton instance"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
