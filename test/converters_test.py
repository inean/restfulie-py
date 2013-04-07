from restfulie.converters import Converters, PlainConverter, \
                                 XmlConverter, JsonConverter


class converters_test:

    def setup(self):
        Converters.types = {}

    def should_register_converters(self):
        converter = PlainConverter()
        Converters.register("text/plain", converter)

        assert Converters.types["text/plain"] == converter

    def test_should_discover_a_for_type_a_type(self):
        assert Converters.for_type("application/atom").__class__ == \
               XmlConverter().__class__
        converter = PlainConverter()
        Converters.register("text/plain", converter)
        assert Converters.for_type("text/plain") == converter


class generic_marshaller_test:

    def should_marshal(self):
        converter = PlainConverter()
        result = converter.marshal("Hello World")
        assert result == "Hello World"

    def should_unmarshal(self):
        converter = PlainConverter()
        result = converter.unmarshal("Hello World")
        assert result == "Hello World"


class json_marshaller_test:

    def should_marshal(self):
        converter = JsonConverter()
        d = {'a': {'c': [1, 2, 3]}, 'b': 2}
        result = converter.marshal(d)
        assert result == '{"a": {"c": [1, 2, 3]}, "b": 2}'

    def should_unmarshal(self):
        converter = JsonConverter()
        json = '{"a": {"c": [1, 2, 3]}, "b": 2}'
        result = converter.unmarshal(json)
        assert result.a.c == [1, 2, 3]
        assert result.b == 2


class xml_marshaller_test:

    def should_marshal(self):
        converter = XmlConverter()
        d = {'html': {'img': ''}}
        result = converter.marshal(d)
        assert result == '<html><img /></html>'

    def should_unmarshal(self):
        xml = XmlConverter()
        result = xml.unmarshal('<html><div><link href="http://google.com" ' +
                               'rel="alternative" type="application/xml">' +
                               'A Link</link><link href="http://yahoo.com" ' +
                               'rel="self" type="application/xml" /></div>' +
                               '<div>Hello World</div>' +
                               '</html>')

        assert result.tag == 'html'
        assert len(result.div) == 2
        assert result.div[0].tag == 'div'
        assert result.div[0].link[0].text == 'A Link'
        assert len(result.div[0].link) == 2
        assert len(result.links()) == 2
