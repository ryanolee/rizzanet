

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
   
    def handle_get_content_type_response(response, as_dict = False):
        response_data = response.as_dict()
        return response_data if as_dict else api_response(response_data)

    


    def handle_commit_transaction():
        '''Handles comitting content to the database and returning error responses on error'''
        try:
            g.db_session.commit()
        except Exception as error:
            g.db_session.rollback()
            return api_error('Error: failed to make changes to db (error:{0}).'.format(error),500) 
        return False


    