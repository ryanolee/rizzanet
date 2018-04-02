from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from flask import render_template,redirect,url_for,flash,request
from functools import wraps
'''Defines core login logic'''
login_manager=LoginManager()
def bind_login(app):
    '''Binds login manager to app'''
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        from rizzanet.models import User
        return User.query.get(int(user_id))

    @app.route('/login/', defaults={'path':''} ,methods=['GET','POST'])
    @app.route('/login/<path:path>',methods=['GET','POST'])
    def login_form_handle(path):
        if current_user.is_authenticated:
            return redirect(path)
        from rizzanet.forms import LoginForm
        form = LoginForm()
        if form.validate_on_submit():
            from rizzanet.models import User
            user=User.query.filter_by(username=form.username.data).first()
            if not user:
                return render_template('forms/login.html', form=form, path=path,error='Username not found.')
            if user.auth(form.password.data):
                login_user(user)
                return redirect(path)
            else:
                return render_template('forms/login.html', form=form, path=path, error='Password invalid.')
        return render_template('forms/login.html', form=form, path=path)
    
    @app.route('/logout')
    @app.route('/logout/')
    @login_required
    def logout():
        logout_user()
        return redirect('/')
def redirect_login_reqired(func):
    '''Redirects to the current full path ('/login/{path}')'''
    @wraps(func)
    def redirect_wrap(*args,**kwargs):
        if current_user.is_authenticated:
            return func(*args,**kwargs)
        else:
            flash('Please log in to contiue')
            return redirect("/login"+request.full_path)
    return redirect_wrap
