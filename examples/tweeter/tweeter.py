# absolute requirements (only because  we are on async mode)
from tornado.ioloop import IOLoop
from datetime import timedelta

# local requirements
from restfulie.client import Client
from apis import *

# Auth pin callback
def get_pin_cb(url):
    print 'Please authorize: ' + url
    verifier = raw_input('PIN: ').strip()
    return verifier

# Call async process
def get_users_cb(response):
    print response.code
    print "UserID", response.resource.id_str

def get_timeline_cb(response):
    print "Timeline Status: ", response.code
    print "Timeline last user:", response.resource, dir(response.resource)

    
if __name__ == "__main__":
    # create client
    client = Client()

    # set credentials
    with client.configure() as conf:
        conf.consumer_key    = "5wXYSVHBaeapdzgCpwrQaw"
        conf.consumer_secret = "xQAOPnRSv1WRMnZBiYtQUDkkSIuSyv3BHYM57FXStjU"
        conf.callback        = get_pin_cb

    # Async call
    client.users("show", {"screen_name" : "qgil"}, get_users_cb)
    #client.users("timeline", {"count" : "5"}, get_timeline_cb)

    # start IOLoop
    IOLoop.instance().add_timeout(timedelta(seconds=20), IOLoop.instance().stop)
    IOLoop.instance().start()
