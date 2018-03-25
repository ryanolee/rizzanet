from flask import jsonify, g
from flask_login import login_required
from sys import setrecursionlimit
setrecursionlimit(1000)
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

    @app.route('/api/get/id/children/<regex("\d+"):parent_id>',methods=['GET'])
    @login_required
    def get_children(parent_id):
        from rizzanet.models import Content
        response=Content.get_by_id(parent_id)
        if response == None:
            return api_error('Error: resource with id {0} not found.'.format(id), 404)
        data = [handle_get_content_response(child,True) for child in response.get_children()]
        return api_response(data)

    @app.route('/api/get/id/subtree/<regex("\d+"):parent_id>',methods=['GET'])
    @login_required
    def get_subtree(parent_id):
        from rizzanet.models import Content
        response=Content.get_by_id(parent_id)
        if response == None:
            return api_error('Error: resource with id {0} not found.'.format(id), 404)
        obj = response.get_subtree()
        def apply_rec(obj):
            to_return = handle_get_content_response(obj,True)
            to_return['children']=[]
            for child in obj.children:
                to_return['children'].append(apply_rec(child))
            if to_return['children'] == []:
                del(to_return['children'])
            return to_return
        return api_response(apply_rec(obj))

    @app.route('/api/create/',methods=['GET','POST'])
    @login_required
    def create_content_object():
        from flask import request
        from rizzanet.models import Content,ContentData
        import json
        required_fields = ['parent_id','name','content_type','content_data']
        for field in required_fields:
            if request.values.get(field) == None:
                return api_error('Error required field {0} not set'.format(field),400)
        parent_id = request.values.get('parent_id')
        parent = Content.get_by_id(parent_id)
        if parent == None:
            return api_error('Error: parent with id {0} not found.'.format(parent_id), 404)
        name = request.values.get('name')
        try:
            data = ContentData.create(request.values.get('content_type'), json.loads(request.values.get('content_data')))
            response = parent.add_child(name,data)
        except Exception:
            g.db_session.rollback()
            return api_error('Error: failed to make changes to db',500)
        res = handle_commit_transaction()
        if res != False:
            return res
        return handle_get_content_response(response) 
    
    def handle_get_content_response(response, as_dict=False):
        content_data = response.get_content_data()
        response_data = {
            'id':response.id,
            'remote_id':response.remote_id,
            'content_type':content_data.get_datatype(),
            'data':content_data.get_data()
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

    def handle_commit_transaction():
        '''Handles comitting content to the database and returning error responses on error'''
        try:
            g.db_session.commit()
        except Exception as error:
            g.db_session.rollback()
            return api_error('Error: failed to make changes to db (error:{0}).'.format(error),500) 
        return False