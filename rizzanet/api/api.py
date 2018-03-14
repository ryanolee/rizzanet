from flask import jsonify
from flask_login import login_required

def bind_api_routes(app):
 
    '''Binds flask routes for api'''
    @app.route('/api/get/path', defaults={'path': ''})
    @app.route('/api/get/path/<path:path>',methods=['GET'])
    @login_required
    def get_by_path(path):
        from rizzanet.models import Content
        response=Content.get_by_path(path.strip('/'))
        if response == None:
             return api_error('Error: resource at path {0} not found.'.format(path), 404)
        return handle_get_content_response(response)

    @app.route('/api/get/id/<regex("\d+"):id>',methods=['GET'])
    @login_required
    def get_by_id(id):
        from rizzanet.models import Content
        response=Content.get_by_id(id)
        if response == None:
            return api_error('Error: resource with id {0} not found.'.format(id), 404)
        return handle_get_content_response(response)

    @app.route('/api/get/id/children/<regex("\d+"):id>',methods=['GET'])
    @login_required
    def get_children(id):
        from rizzanet.models import Content
        response=Content.get_by_id(id)
        if response == None:
            return api_error('Error: resource with id {0} not found.'.format(id), 404)
        data = [handle_get_content_response(child,True) for child in response.get_children()]
        return api_response(data)
    def handle_get_content_response(response, as_dict=False):
        response_data = {
            'id':response.id,
            'remote_id':response.remote_id,
            'content_type':response.content_data.get_datatype(),
            'data':response.content_data.get_data()
        }
        return response_data if as_dict else api_response(response_data)
    def api_error(error_message,code):
        return jsonify(
            code=code,
            error_message=error_message
        ), code
    def api_response(data,code=200):
        response_dict={'code':code,'result':data}
        return jsonify(**response_dict), code