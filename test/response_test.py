from restfulie.response import Response
from tornado.httpclient import HTTPResponse

class response_test:
    
    def trivial_test(self):
    
        response = HTTPResponse(None, 'code'=200, body='Hello')
    
        r = Response(response)
        assert r.body == 'Hello'
        assert r.code == 200
    
    
    def resource_test(self):
    
        response = ({'code': 200, 'content-type': \
                     'text/plain; charset=utf-8'}, 'Hello')
    
        r = Response(response)
        assert r.resource() == 'Hello'
    
    
    def link_test(self):
    
        response = ({'code': 200, 'link': '</feed>; rel="alternate"'}, 'Hello')
        r = Response(response)
        link = r.link('alternate')
        assert link.href == '/feed'
        assert link.rel == 'alternate'
