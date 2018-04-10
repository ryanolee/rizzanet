from flask import jsonify, g
from flask_login import login_required
from flask_cors import CORS
from sys import setrecursionlimit

setrecursionlimit(1000)
def bind_api_routes(app):
    '''Binds flask routes for api'''
    CORS(app, resources=r'/api/*')
    def api_auth(func):
        '''Handles auth for Api'''
        from functools import wraps
        @wraps(func)
        def auth_wrap(*args,**kwargs):
            from flask_login import current_user
            if current_user.is_authenticated and current_user.role > 1000:
                return func(*args,**kwargs)
            from flask import request
            api_key = request.values.get('api_key')
            if api_key == None:
                return api_error('No api key given', 403)
            from rizzanet.models import APIKey
            try:
                key = APIKey.get_by_api_key(api_key)
                authenticated = key.auth(api_key)
            except Exception as error:
                return api_error('Error: authentication failed {0}'.format(error))
            if not authenticated:
                return api_error('Api key invalid', 403)
            return func(*args,**kwargs)
        return auth_wrap

    def required_fields(func,*required_field_data):
        '''Handles auth for Api'''
        def arg_wrapper(func):
            '''partial func so that decorator can be invoked'''
            from functools import wraps
            @wraps(func)
            def required_wrap(*args,**kwargs):
                from flask import request
                to_return = []
                for field in required_field_data:
                    if request.values.get(field) == None:
                        to_return.append("'"+field+"'")
                if to_return != []:  
                    return api_error('Error required field{0} {1} not set'.format('' if len(to_return)==1 else 's' ,','.join(to_return)),400)
                return func(*args,**kwargs)
            return required_wrap
        return arg_wrapper
        
    @app.route('/api/get/path', defaults={'path': ''})
    @app.route('/api/get/path/<path:path>',methods=['GET','FETCH'])
    @api_auth
    def get_by_path(path):
        from rizzanet.models import Content
        response=Content.get_by_path(path.strip('/'))
        if response == None:
             return api_error('Error: resource at path {0} not found.'.format(path), 404)
        return handle_get_content_response(response)

    @app.route('/api/get/id/<regex("\d+"):id>',methods=['GET','FETCH'])
    @api_auth
    def get_by_id(id):
        from rizzanet.models import Content
        response=Content.get_by_id(id)
        if response == None:
            return api_error('Error: resource with id {0} not found.'.format(id), 404)
        return handle_get_content_response(response)

    @app.route('/api/get/id/children/<regex("\d+"):parent_id>',methods=['GET','FETCH'])
    @api_auth
    def get_children(parent_id):
        from rizzanet.models import Content
        response=Content.get_by_id(parent_id)
        if response == None:
            return api_error('Error: resource with id {0} not found.'.format(parent_id), 404)
        data = [handle_get_content_response(child,True) for child in response.get_children()]
        return api_response(data)

    @app.route('/api/get/id/subtree/<regex("\d+"):parent_id>',methods=['GET','FETCH'])
    @api_auth
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
    @api_auth
    @required_fields('parent_id','name','content_type','content_data')
    def create_content_object():
        from flask import request
        from rizzanet.models import Content,ContentData
        import json
        parent_id = request.values.get('parent_id')
        parent = Content.get_by_id(parent_id)
        if parent == None:
            return api_error('Error: parent with id {0} not found.'.format(parent_id), 404)
        name = request.values.get('name')
        try:
            data = ContentData.create(request.values.get('content_type'), json.loads(request.values.get('content_data')))
            response = parent.add_child(name,data)
        except Exception as error:
            g.db_session.rollback()
            return api_error('Error: failed to make changes to db %s' % error,500)
        res = handle_commit_transaction()
        if res != False:
            return res
        return handle_get_content_response(response) 
    
    def handle_get_content_response(response, as_dict=False):
        try:
            parts = get_parts()
        except Exception as error:
            return api_error('Error: invalid parts format.',400)
        response_data = {
            'id':response.id,
            'remote_id':response.remote_id,
            'name':response.name
        }
        if parts != False:
            if any([ part in parts for part in ['all','content_data']]):
                content_data = response.get_content_data()
                response_data['data'] = content_data
            if any([ part in parts for part in ['all','content_type']]):
                from rizzanet.models import ContentType
                response_data['content_type'] = ContentType.get_content_type_from_mixed(response.content_type_id)
        return response_data if as_dict else api_response(response_data)

    def api_error(error_message,code=500):
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

    def get_parts():
        '''gets parts for content objects'''
        from flask import request
        valid_parts = ['content', 'content_data', 'content_type', 'all']
        parts = request.values.get('parts')
        if parts == None:
            return False
        parts = parts.split(',')
        if len(parts) == 0 or not all([part in valid_parts for part in parts]):
            raise Exception('Invalid format for parts')
        else:
            return parts
    