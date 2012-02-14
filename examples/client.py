from restfulie.restfulie import Restfulie
response = Restfulie.at("http://localhost:8080").accepts("application/json").get()
r = response.resource
print r.status
print r.servertime
print r.link('self')
a = response.links.follow().get()
for link in a.links:
    print link
print a


