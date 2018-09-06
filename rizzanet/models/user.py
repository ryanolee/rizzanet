from sqlalchemy import Column,String,Integer,Binary
from rizzanet.db import Base
from flask_login import UserMixin
import bcrypt

class User(Base,UserMixin):
    __tablename__ = 'Users'
    id = Column(Integer,  primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    role=Column(Integer)
    _password = Column(Binary)
    def __init__(self,name,username,password,role):
        self.name = name
        self.username = username
        self._password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        self.role=role
    def __repr__(self):
        return '<User(id:%r,name:%r,username:%r,password:-,role:%r)>' % self.id,self.name,self.username,self.role
    def auth(self,password):
        return bcrypt.checkpw(password.encode(), self._password)