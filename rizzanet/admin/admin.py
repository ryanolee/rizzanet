
from flask_login import login_required
from rizzanet.login import redirect_login_reqired
from flask import render_template,url_for
def bind_admin_routes(app):
    @app.route('/admin')
    @app.route('/admin/')
    @redirect_login_reqired
    def admin():
        return
