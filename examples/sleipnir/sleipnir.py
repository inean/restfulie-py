#!/usr/bin/env python
# -*- coding: utf-8 -*-

# absolute requirements (only because  we are on async mode)
from tornado.ioloop import IOLoop
from datetime import timedelta

# local requirements
from restfulie.client import Client
from hipermedia.apis  import *

# sugar
from functools import partial, wraps
from pprint import pprint

# for HTTP codes and messages only
import httplib

# simple decorator to exit application
def stop(func):
    """check that all calls has been executed. If so, stop loop"""
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        IOLoop.instance().total_calls -= 1
        if not IOLoop.instance().total_calls:
            IOLoop.instance().stop()
    return wrapper

# Auth pin callback
def get_pin_cb(url):
    print 'Please authorize: ' + url
    verifier = raw_input('PIN: ').strip()
    return verifier

# Call async process
@stop
def get_users_cb(method, response):
    print "\nResponse to call '%s':" % method
    print "  Status %d: %s" %(response.code, httplib.responses[response.code])
    IOLoop.instance().total_calls

    if response.code in (httplib.OK, httplib.NO_CONTENT,):
        if method == 'show':
            print "  User ID", response.resource.user.id
        print '  links (%d):' % len(response.links),  str([str(link) for link in response.links])
    else:
        if response.error.details:
            for line in response.error.details.traceback:
                print line[:-1]
        else:
            print "Error message: ", response.error.value

@stop
def get_search_cb(method, response):
    print "\nResponse to call '%s':" % method
    print "  Status %d: %s" %(response.code, httplib.responses[response.code])
    if response.code == httplib.OK:
        pprint(response.resource._dict)
    
if __name__ == "__main__":
    # create client
    client = Client()

    # set credentials
    with client.configure() as conf:
        conf.consumer_key           = "5wXYSVHBaeapdzgCpwrQaw"
        conf.consumer_secret        = "xQAOPnRSv1WRMnZBiYtQUDkkSIuSyv3BHYM57FXStjU"
        conf.oauth_callback         = "oob"
        conf.oauth_callback_handler = get_pin_cb
        #conf.token_key       = "iEqwrSFzXGkY3eKehpbtPw"
        #conf.token_secret    = "pLaQ2sn9PT0WAodk0c6zxmWMTahqeM7Xwjj7Tp7JofA"

    #gFIXME: Implement this
    #net = client.authenticate()
    #net.cancel()
    
    # Async auth call
    client.persons("search",
                   {"query" : "'car'"},
                   partial(get_search_cb, "search")
    )
    # Async call
    with file("avatar.png") as f:
        client.users("show",
                     {"username" : "usal"},
                     partial(get_users_cb, "show")
        )
        client.users("show_authorized",
                    {"username" : "usal"},
                     partial(get_users_cb, "show_authorized")
        )
        client.users("update",
                     {"username" : "usal", "surname": "Martín", "avatar" : f},
                     partial(get_users_cb, "update")
        )

    # start IOLoop
    IOLoop.instance().total_calls = 4
    IOLoop.instance().add_timeout(timedelta(seconds=20), IOLoop.instance().stop)
    IOLoop.instance().start()
