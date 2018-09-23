
def bind_jinja2_functions(app):

    @app.context_processor
    def utility_processor():
        def get_content_by_id(id):
            '''gets content by id'''
            from rizzanet.models import Content
            try:
                return dict(Content.get_by_id(id))
            except:
                return None

        def get_content_data_by_id(id):
            '''gets content data by id'''
            from rizzanet.models import ContentData
            try:
                return ContentData.get_by_id(id).as_dict()
            except:
                return None
        
        def get_content_type_by_id(id):
            from rizzanet.models import ContentType
            try:
                return ContentType.get_by_id(id).as_dict()
            except:
                return None
        
        def get_children(id,**kwargs):
            '''get children of an object'''
            from rizzanet.models import Content
            content_object = Content.get_by_id(id)
            to_return = []
            for child in content_object.get_children():
                data = child.as_dict()
                if kwargs.get('content_data',False):
                    data['content_data'] = child.get_content_data().as_dict()
                to_return.append(data)
            return to_return
        
        def get_subtree(id,**kwargs):
            '''get content object subtree'''
            from rizzanet.models import Content
            content_object = Content.get_by_id(id)
            return content_object.get_subtree(as_dict=True,**kwargs)
        
        def get_path(path):
            from rizzanet.models import Content
            return Content.get_by_path(path)
        
        def get_image_url(image, alias=None):
            from rizzanet.helpers import ImageHelper
            return ImageHelper(app).get_image_uri(image, alias)

        def get_render_context():
            from rizzanet.core.context import get_render_context
            render_ctx = get_render_context()
            return render_ctx.current()
            

        return dict(
            get_content = get_content_by_id,
            get_content_data = get_content_data_by_id,
            get_content_type = get_content_type_by_id,
            get_children = get_children,
            get_subtree = get_subtree,
            get_path = get_path,
            get_image_url = get_image_url
        )
            