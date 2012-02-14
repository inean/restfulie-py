import time
from bottle import route, run, debug

@route('/')
def index():
    return {
        'status':'online',
        'servertime':time.time(),
        'link': [
            { 'rel': 'self', 'href': 'http://localhost:8080/' },
            { 'rel': 'payment', 'href': 'http://localhost:8080/payment' },
        ],
    }

debug(True)
run(host='localhost', port=8080)
