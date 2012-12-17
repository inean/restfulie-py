from restfulie.restfulie import Restfulie
from tornado.ioloop import IOLoop

found = False
visited = {}
steps = 0

def solve(current):
    global found
    global visited
    if not found and not current.link('exit'):
        directions = ["start", "east", "west", "south", "north"]
        for direction in directions:
            link = current.link(direction)
            if not found and link and not visited.get(link.href):
                visited[link.href] = True
                link.follow().get(callback=solve)

    else:
        IOLoop.instance().stop()
        print "FOUND!"
        found = True

# syncronous invoke
current = Restfulie.at('http://amundsen.com/examples/mazes/2d/five-by-five/').accepts("application/xml").get()

# async invoke
solve(current)

# start IOLoop
IOLoop.instance().start()
