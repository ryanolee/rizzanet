from flask.json import JSONEncoder
class APIJSONEncoder(JSONEncoder):
    def default(self, obj):
        if callable(getattr(obj, 'as_dict', None)):
            return {name: self.default(val) for name, val in obj.as_dict().items()}
        if not isinstance(obj, dict):
            return obj
        return JSONEncoder.default(self, obj)