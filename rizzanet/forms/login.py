from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Length
from wtforms import StringField, PasswordField, BooleanField, HiddenField
class LoginForm(FlaskForm):
    username=StringField('Username:',validators=[Length(min=1,max=15, message='Error: usernames between %(min)d and %(max)d charicters in length.')])
    password=PasswordField('Password:',validators=[Length(min=1,max=80)])
    remember_me=BooleanField('Remember me')


