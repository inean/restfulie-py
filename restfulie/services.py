# -*- mode:python; coding: utf-8 -*-

"""
Services
"""

from __future__ import absolute_import

__author__ = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# required modules
import os
import numbers
import urlparse
import operator
import itertools
import collections

__all__ = ['Services']

# Import here local requirements
from .cached import cached


class FrozenDict(collections.Mapping):
    """A wrapper around a dict to create inmmutable dicts"""

    def __init__(self, *args, **kwargs):
        self.__dict = dict(*args, **kwargs)
        self.__hash = None

    def __getitem__(self, key):
        return self.__dict[key]

    def __setitem__(self, key):
        raise RuntimeError("Unable to set items: Frozen dict")

    def __delitem__(self, key):
        raise RuntimeError("Unable to delete items: Frozen dict")

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __repr__(self):
        return '<frozendict %s>' % repr(self.__dict)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = reduce(
                operator.xor,
                itertools.imap(hash, self.iteritems()),
                0)
        return self.__hash


# pylint: disable-msg=R0903
class Services(object):
    """
    Services configuration class. Provides information about available
    services location and security requirements
    """

    # Currently allowed service description keys
    SERVICE_ITEMS = [
        'protocol',
        'host',
        'path',
        'port',
        'secure_port',
        'ca_certs',
        'enforce',
    ]

    def __init__(self):
        self._urls = {}

    def __iter__(self):
        return self._urls.iteritems()

    def __contains__(self, key):
        return key in self._urls

    @cached
    def service(self, name):
        """Fetch a service"""
        retval = self._urls.get(name)
        return retval or FrozenDict(retval)

    def register(self, services):
        """
        Register collection of services. Override current values if
        already exists
        """
        self._urls.update(services)

    def set_service_item(self, key, value, services=None):
        """
        Update key, value pair for services
        """
        if key not in self.SERVICE_ITEMS:
            raise AttributeError("Invalid service key '{0}'".format(key))

        # selective update
        if services:
            assert isinstance(services, collections.Sequence)
            services = itertools.ifilter(lambda x: x in self._urls, services)
        # update all
        services = services or self._urls.iterkeys()
        # pylint: disable-msg=W0106
        [self._urls[service].update([(key, value)]) for service in services]

    def get_url(self, service, extra_path=None, query=None, fragment=None):
        """
        Build an url for a service. If extra_path is an absolute path,
        path from service will be ignored
        """

        # fetch service instance
        service = self._urls.get(service)
        if service:
            # get protocol
            protocol = service.get('protocol', 'http')
            port = 'secure_port' if protocol == 'https' else 'port'
            # get netloc
            host = service['host']
            port = service.get(port)
            # if it's a valid port number, get a better netloc'
            if isinstance(port, numbers.Integral):
                host = "{0}:{1}".format(host, port)
            # build path
            path = service.get('path', '')
            if extra_path:
                path = extra_path if extra_path[0] == '/' \
                    else os.path.join(path, extra_path)
            # build it;
            return urlparse.urlunsplit((protocol, host, path, query, fragment))
        # No service
        return None

    @cached
    def get_secure(self, service, secure=None, port=None, ca_certs=None):
        """Get a secure tuple as required by secure method of restfulie"""

        # if enforce is set, base is ignored
        ssecure = self._urls[service].get('protocol') == 'https'
        sport = self._urls[service].get('secure_port' if ssecure else 'port')
        sca_certs = self._urls[service].get('ca_certs') if ssecure else None
        if self._urls[service].get('enforce', False):
            return [ssecure, sport, sca_certs]

        # Get base values
        retval = [secure, port, ca_certs]

        # Override port, if base defines some kind of security None
        # means leave 'as is'
        if retval[0] is not None:
            port = 'port'
            if retval[0]:
                port = 'secure_port'
            # override port
            retval[1] = retval[1] or self._urls[service].get(port)

        #if retval[0] or retval[0] is None and ssecure:
        # Add ca_certs if no one is set and https or 'as is' is required
        retval[2] = retval[2] or sca_certs

        # done!
        return retval

    @classmethod
    def get_instance(cls):
        """Get service singleton instance"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
