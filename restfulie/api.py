# -*- mode:python; tab-width: 2; coding: utf-8 -*-

"""
BaseAPI
"""

from __future__ import absolute_import

__author__  = "Carlos Martin <cmartin@liberalia.net>"
__license__ = "See LICENSE.restfulie for details"

# Import here any required modules.
from itertools import ifilter, imap

__all__ = ['BaseAPI', 'BaseMapper']

# Project requirements
from .restfulie import Restfulie
from .services import Services

# Create:
#-------.
# PUT:  if you are sending the full content of the specified resource (URL).
# POST: if you are sending a command to the server to create a
#       subordinate of the specified resource, using some server-side
#       algorithm.

# Retrieve
# --------
# GET

# Update
# -------
# PUT:   if you are updating the full content of the specified resource.
# PATCH: if you are requesting the server to update one or
#        more subordinates of the specified resource.

# Delete
# ------
# DELETE.


# pylint: disable-msg=R0903
class BaseAPI(object):
    """
    Derive from here Custom API Implementations. All implementations
    MUST be stateless
    """

    # Which Urls from Client's URLS class attribute should be used
    # when computing invoke endpoint. It's an alias for a service. We
    # must use Targets to translate this alias into a valid service
    TARGET  = None
    # A service is an URL and a CACert file registered in Session
    SERVICE = None

    # Rest smells
    FLAVORS  = None
    CHAIN    = None
    COMPRESS = False

    # Timeouts
    CONNECT_TIMEOUT = None
    REQUEST_TIMEOUT = None

    @classmethod
    def __create(cls, client, endpoint):
        """Build REST request with safe defaults"""

        return Restfulie.at(
            uri=endpoint,
            flavors=cls.FLAVORS,
            chain=cls.CHAIN,
            compress=cls.COMPRESS,
            ca_certs=cls.__cacert(client),
            connect_timeout=cls.CONNECT_TIMEOUT,
            request_timeout=cls.REQUEST_TIMEOUT
        )

    @classmethod
    def __base_url(cls, client, default=""):
        """Get base url for Target / Service combination"""
        url_key = client.TARGETS.get(cls.TARGET, cls.SERVICE)
        return Services.get_instance().URLS.get(url_key, default)

    @classmethod
    def __cacert(cls, client):
        """Get cacert, if any for Target / Service combination"""
        ca_cert = client.TARGETS.get(cls.TARGET, cls.SERVICE)
        return Services.get_instance().CACERTS.get(ca_cert)

    #pylint: disable-msg=C0301, R0913, W0142
    @classmethod
    def _get(cls, client, auth, endpoint, flavor, compress,
             secure, timeout, args, callback):
        """Implementation of verb GET"""

        return cls.__create(client, endpoint)         \
            .secure(*secure)                          \
            .auth(client.credentials, method=auth)    \
            .accepts(flavor)                          \
            .until(*timeout)                          \
            .compress(compress)                       \
            .get(callback=callback, params=args)

    #pylint: disable-msg=C0301, R0913, W0142
    @classmethod
    def _post(cls, client, auth, endpoint, flavor, compress,
              secure, timeout, args, callback):
        """Implementation of verb POST"""

        #default to form-urlencode. If somthing that smells like a
        #file (has read function) is pased in args, encode it as
        #multipart form

        return cls.__create(client, endpoint)         \
            .secure(*secure)                          \
            .as_(flavor)                              \
            .auth(client.credentials, method=auth)    \
            .until(*timeout)                          \
            .compress(compress)                       \
            .post(args, callback=callback)

    #pylint: disable-msg=C0301, R0913, W0142
    @classmethod
    def _put(cls, client, auth, endpoint, flavor, compress,
             secure, timeout, args, callback):
        """Implementation of verb PUT"""

        #default to form-urlencode. If somthing that smells like a
        #file (has read function) is pased in args, encode it as
        #multipart form

        return cls.__create(client, endpoint)         \
            .secure(*secure)                          \
            .as_(flavor)                              \
            .auth(client.credentials, method=auth)    \
            .until(*timeout)                          \
            .compress(compress)                       \
            .put(args, callback=callback)

    #pylint: disable-msg=C0301, R0913, W0142
    @classmethod
    def _patch(cls, client, auth, endpoint, flavor, compress,
               secure, timeout, args, callback):
        """Implementation of verb PATCH"""

        # JSON path expexts an array of objects. Internally, We need
        # to pass Request object will asumme that we are providing an
        # array if args is defined as a length 1 dict with None as key
        # See also:
        # https://datatracker.ietf.org/doc/draft-ietf-appsawg-json-patch/

        return cls.__create(client, endpoint)         \
            .secure(*secure)                          \
            .as_(flavor)                              \
            .auth(client.credentials, method=auth)    \
            .until(*timeout)                          \
            .compress(compress)                       \
            .patch(args, callback=callback)

    #pylint: disable-msg=C0301, R0913, W0142
    @classmethod
    def _delete(cls, client, auth, endpoint, flavor, compress,
                secure, timeout, args, callback):
        """Implementation of verb DELETE"""

        return cls.__create(client, endpoint)         \
            .secure(*secure)                          \
            .auth(client.credentials, method=auth)    \
            .accepts(flavor)                          \
            .until(*timeout)                          \
            .compress(compress)                       \
            .get(callback=callback, params=args)

    #pylint: disable-msg=C0301, R0913, W0142
    @classmethod
    def invoke(cls, client, call, body, args, callback=None):
        """Invoke method"""

        def _endpoint(endpoint):
            """Compute endpoint if a relative one is pushed"""
            if not endpoint.startswith('http'):
                # only absolute paths are allowed
                assert endpoint[0] == '/'
                endpoint = cls.__base_url(client) + endpoint
            return endpoint

        def _peek(value, target, *composition):
            """Peek a collection of values"""
            retval = value.get(target, [])
            if isinstance(retval, dict):
                retval = list(imap(retval.get, composition))
            if not type(retval) in (list, tuple,):
                retval = [retval]
            return retval

        # parse requirements
        for req in ifilter(lambda x: x not in args, call.get("required", ())):
            raise AttributeError(
                "Missing args '%s' for '%s' call" % (req, call)
            )

        # substitute endpoint args
        path = call.get("endpoint", "/")
        endpoint = path % args

        # remove used args
        func = lambda x: '%%(%s)' % x[0] not in path
        args = dict(ifilter(func, args.iteritems()))

        # we allow only, body or args, bbut not both
        if args and body:
            raise AttributeError(
                "Args provided on a call with content. Unable to determine "
                "which one should be used. Body:'' Args:'%s'", body, repr(args)
            )

        # check if body content is required
        if call.get("body", False) and body is None:
            raise AttributeError("Missing body content")

        # invoke!!
        return getattr(cls, "_" + call["method"])(
            client=client,
            auth=call.get("auth"),
            endpoint=_endpoint(endpoint),
            flavor=call.get("flavor"),
            compress=call.get("compress"),
            secure=_peek(call, "secure", "value", "port", "ca_certs"),
            timeout=_peek(call, "timeout", "connect_timeout", "request_timeout"),
            args=body or args,
            callback=callback
        )


class BaseMapper(object):
    """Sugar class to allow a more pythonic way to invoke REST Api"""

    API = None

    def __init__(self, client, api, ignore=None):
        self.__client = client
        self.__api    = api
        self.__ignore = ignore or []

    def __iter__(self):
        self.__api.iterkeys()

    def __setattr__(self, key, value):
        if key[0] != '_':
            raise AttributeError(key)
        return object.__setattr__(self, key, value)

    def __getattr__(self, action):

        def invoke(*args, **kwargs):
            """Invoke api"""
            args     = list(args)
            params   = kwargs
            callback = params.pop("callback", None)
            # If callback isn't passed as keyword argument, try to
            # fetch from args
            if not callback and args and callable(args[-1]):
                callback = args.pop(-1)
            for req in self.__api[action].get("required", ()):
                if args and req not in params:
                    params.setdefault(req, args.pop(0))

            assert len(args) <= 1
            body = args[0] if args else None

            return self.API.invoke(
                self.__client, self.__api[action], body, params, callback)

        # validate
        if action not in self.__api:
            raise AttributeError("Missing action '%s'" % action)
        if action in self.__ignore:
            raise AttributeError("Invalid API call '%s'" % action)
        return invoke
