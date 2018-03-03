
from flask import render_template,url_for
def register_routes(app):
    """Registers routes for the core set of pages for the app"""
    @app.route('/')
    def index():
        return render_template('pages/index.html')

