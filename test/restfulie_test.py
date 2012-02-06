from restfulie.restfulie import Restfulie
from restfulie.configuration import Configuration


class restfulie_test:

    def should_return_a_dsl_object(self):
        assert type(Restfulie.at("www.caelum.com.br")) == Configuration
