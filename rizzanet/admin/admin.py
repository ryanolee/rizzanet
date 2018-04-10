
from flask_login import login_required
from rizzanet.login import redirect_login_reqired
from flask import send_from_directory
import os
def bind_admin_routes(app):
    '''binds admin routes'''
    @app.route('/admin/', defaults={'path': ''})
    @app.route('/admin/<path:path>',methods=['GET'])
    @redirect_login_reqired
    def admin(path):
        print('from os dir')
        if path == "":
            return send_from_directory( 'rizzanet/admin/admin_app/build/', 'index.html')
        elif os.path.exists('rizzanet/admin/admin_app/build/' + path):
            return send_from_directory('rizzanet/admin/admin_app/build/', path)
        else:
            return send_from_directory('rizzanet/admin/admin_app/build/', 'index.html')
