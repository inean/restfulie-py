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
from re import search

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
        super(Link, self).__setattr__('_dict', data)

    def __setattr__(self, key, value):
        key = key if key != 'content_type' else 'type'
        self._dict[key.replace('_', '-')] = value

    def __getattr__(self, key):
        key = key if key != 'content_type' else 'type'
        return self._dict[key.replace('_', '-')]

    def __str__(self):
        return "'%s' (%s) => %s" % (self.rel, self.type, self.href,)

    def follow(self):
        """Return a DSL object with the Content-Type set"""
        from .configuration import Configuration
        return Configuration(self.href).as_(self.content_type)

    @staticmethod
    def parse(link_string):
        """Parses a link header string to a dictionary"""
        try:
            uri  = search('<([^>]*)', link_string).group(1)
            rest = search('.*>(.*)', link_string).group(1)
            rel  = search('rel="(.*)"', rest).group(1)
            tpe  = search('type="(.*)"', rest).group(1)
        except AttributeError:
            return None
        return Link(href=uri, rel=rel, content_type=tpe)


#pylint: disable-msg=R0903
class Links(object):
    """Links a simple Link """

    def __init__(self, links):
        self._links = {}
        self.update(links)

    def __iter__(self):
        return self._links.itervalues()

    def __len__(self):
        return len(self._links)

    def __getattr__(self, value):
        raise LinkError("'%s' link is missing or malformed" % value)

    def get(self, rel):
        """Checks Link existence"""
        return self._links.get(rel)

    def update(self, links):
        """Update links with links"""
        for link in links:
            if hasattr(link, 'rel') and hasattr(link, 'href'):
                self._links[link.rel] = link
                setattr(self, link.rel, link)
