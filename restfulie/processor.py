from base64 import encodestring
from response import Response
from converters import Converters
from tornado.httpclient import HTTPClient, AsyncHTTPClient
import restfulie


class RequestProcessor(object):
    def execute(self, callback, chain, request, env={}):
        raise NotImplementedError('Subclasses must implement this method')


class AuthenticationProcessor(RequestProcessor):
    """
    Processor responsible for making HTTP simple auth
    """
    def execute(self, callback, chain, request, env={}):
        if request.credentials is not None:
            encoded_credentials = self._encode_credentials(request.credentials)
            request.headers['authorization'] = "Basic %s" % encoded_credentials
        return chain.follow(callback, request, env)

    def _encode_credentials(self, credentials):
        username = credentials[0]
        password = credentials[1]
        method = credentials[2]
        if (method == 'simple'):
            return encodestring("%s:%s" % (username, password))[:-1]


class ExecuteRequestProcessor(RequestProcessor):
    """
    Processor responsible for getting the body from environment and
    making a request with it.
    """
    def _sync(self, chain, request, env={}):
        response = HTTPClient().fetch(
            request.uri,
            method=request.verb,
            body=env.get("body"), 
            headers=request.headers)
        return Response(response)

    def _async(self, callback, chain, request, env={}):
        AsyncHTTPClient().fetch(
            request.uri,
            lambda x: callback(Response(x)),
            method=request.verb,
            body=env.get("body"), 
            headers=request.headers)
        return None

    def execute(self, callback, chain, request, env={}):
        return self._sync(chain, request, env) \
            if not callable(callback)          \
            else self._async(callback, chain, request, env)


class PayloadMarshallingProcessor(RequestProcessor):
    """
    Processor responsible for marshalling the payload in environment.
    """
    def execute(self, callback, chain, request, env={}):
        if "payload" in env:
            content_type = request.headers.get("Content-Type")
            marshaller = Converters.marshaller_for(content_type)
            env["body"] = marshaller.marshal(env["payload"])
            del(env["payload"])

        return chain.follow(callback, request, env)


class RedirectProcessor(RequestProcessor):
    """
    A processor responsible for redirecting a client to another URI when the
    server returns the location header and a response code related to
    redirecting.
    """
    REDIRECT_CODES = ['201', '301', '302']

    def redirect_location_for(self, result):
        if (result.code in self.REDIRECT_CODES):
            return (result.headers.get("Location") or
                    result.headers.get("location"))
        return None

    def execute(self, callback, chain, request, env={}):
        def _on_resource(resource):
            assert callable(callback)
            location = self.redirect_location_for(resource)
            return callback(resource) if not location else \
                restfulie.Restfulie.at(location).as_(request_type).get(callback)
        # chain
        return chain.follow(_on_resource, request, env)    \
            if callable(callback) else chain.follow(callback, request, env)

