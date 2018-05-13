
from flask import render_template,url_for,abort
def register_routes(app):
    """Registers routes for the core set of pages for the app"""

    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>',methods=['GET','POST'])
    def load_location(path):
        '''Catch all that loads content locations last location registered'''
        from rizzanet.models import Content
        response=Content.get_by_path(path)
        if response == None:
            return abort(404)
        else:
            return response.render()
