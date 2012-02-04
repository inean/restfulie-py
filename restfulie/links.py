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

__all__ = ['Link', 'Links', 'HeaderLinks']

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

    @staticmethod
    def parse(link_string):
        """Parses a link header string to a dictionary"""
        uri  = search('<([^>]*)', link_string).group(1)
        rest = search('.*>(.*)', link_string).group(1)
        rel  = search('rel="(.*)"', rest).group(1)
        tpe  = search('type="(.*)"', rest).group(1)
        return Link(href=uri, rel=rel, content_type=tpe)


#pylint: disable-msg=R0903
class Links(object):
    """Links a simple Link """

    def __init__(self, links):
        self.links = {}
        self.update(links)

    def __len__(self):
        return len(self.links)

    def __getattr__(self, value):
        raise LinkError("'%s' link is missing or malformed" % value)

    def get(self, rel):
        """Checks Link existence"""
        return self.links.get(rel)

    def update(self, links):
        """Update links with links"""
        for link in links:
            if hasattr(link, 'rel') and hasattr(link, 'href'):
                self.links[link.rel] = link
                setattr(self, link.rel, link)


class HeaderLinks(object):
    """Links from headers """

    # pylint: disable-msg=W0106
    def __init__(self, header):
        links, values = [], header.get_list('link')
        [links.append(Link.parse(link)) for link in values]
        self._links = links

    def __iter__(self):
        return iter(self._links)


