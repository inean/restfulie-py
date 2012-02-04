#!/usr/bin/env python
# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
links

Hipermedia objrects
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE file for details"

# Import here any required modules.

__all__ = ['Link', 'Links']

# Project requirements

# local submodule requirements

class LinkError(Exception):
    """Define a missing link error"""


#pylint: disable-msg=R0903
class Link(object):
    """Link represents generic link. You can follow it"""

    def __init__(self, data):
        assert isinstance(data, dict)
        self._dict = data

    def __getattr__(self, key):
        key = key if key != 'content_type' else 'type'
        return self._dict[key.replace('_', '-')]

    def follow(self):
        """Return a DSL object with the Content-Type set"""
        from .configuration import Configuration
        return Configuration(self.href).as_(self.content_type)


#pylint: disable-msg=R0903
class Links(object):
    """Links a simple Link """

    def __init__(self, links):
        self.links = {}
        for link in links:
            if hasattr(link, 'rel') and hasattr(link, 'href'):
                self.links[link.rel] = link
                setattr(self, link.rel, link)

    def __getattr__(self, value):
        raise LinkError("'%s' link is missing or malformed" % value)

    def __len__(self):
        return len(self.links)

    def get(self, rel):
        """
        Checks if a Link exists. If exists returns the object, else
        returns None
        """
        return self.links.get(rel)

