from flask import jsonify, g
from flask_login import login_required
from flask_cors import CORS
from sys import setrecursionlimit
from rizzanet.api.controllers import content_controller
from .json_serializer import APIJSONEncoder
import re

setrecursionlimit(1000)
def init(app):
    '''Binds flask routes for api'''
    app.json_encoder = APIJSONEncoder 
    url_prefix = '/api/' + app.config['API_VERSION']
    CORS(app, resources=re.compile(url_prefix+'*'))
    app.register_blueprint(content_controller, url_prefix = url_prefix + content_controller.url_prefix)
    
        
    