from response import LazyResponse
from parser import Parser

class Request(object):
    """
    HTTP request.
    """

    def __init__(self, config):
        """
        Initialize an HTTP request instance for a given configuration.
        """
        self.config = config

    def __call__(self, callback=None, **payload):
        """
        Perform the request

        The optional payload argument is sent to the server.
        """
        env = {}
        if payload:
            env = {'payload': kwargs}

        procs = list(self.config.processors)
        return Parser(procs).follow(callback, self.config, env)
