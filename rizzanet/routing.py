from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
def bind_converters_to_app(app):
    app.url_map.converters['regex'] = RegexConverter
