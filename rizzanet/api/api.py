from flask import jsonify
from flask_login import login_required

def bind_api_routes(app):
 
    '''Binds flask routes for api'''
    @app.route('/api/get/path', defaults={'path': ''})
    @app.route('/api/get/path/<path:path>',methods=['GET'])
    @login_required
    def get_by_path(path):
        from rizzanet.models import Content
        response=Content.get_by_path(path)
        if response == None:
             return jsonify()
        return jsonify(
            id=response.id,
            remote_id=response.remote_id
        )