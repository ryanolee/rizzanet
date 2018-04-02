from sqlalchemy import Column,String,Integer
from rizzanet.db import Base
from flask import g
import bcrypt

class APIKey(Base):
    __tablename__ = 'APIKey'
    id = Column(Integer,  primary_key=True)
    api_key = Column(String)

    def __init__(self,key):
        self.api_key = bcrypt.hashpw(key.encode(),bcrypt.gensalt())

    def __repr__(self):
        return '<APIKey>' 

    def auth(self,key):
        api_key = self.from_base64(key)
        api_key = api_key.split('__')
        if len(api_key) <= 1:
            raise Exception('Error api key invalid. Missing (id)__')
        key = ''.join(api_key[1:])
        return bcrypt.checkpw(key.encode(),self.api_key)
    
    @classmethod
    def create(self,key):
        api_key = self(key)
        g.db_session.add(api_key)
        g.db_session.flush()
        g.db_session.refresh(api_key)
        return api_key
    
    @classmethod
    def get_by_id(self,id):
        try:
            api_key = g.db_session.query(self).filter( self.id ==  id).one()
        except Exception as error:
            raise Exception('Error no api key found with id:{0} error: {1}'.format( id,error))
        return api_key
    
    @classmethod
    def get_by_api_key(self,api_key):
        
        api_key = self.from_base64(api_key)
        api_key = api_key.split('__')
        if len(api_key) <= 1:
            raise Exception('Error api key invalid. Missing (id)__')
        return self.get_by_id(int(api_key[0]))
    
    @staticmethod
    def to_base64(api_key):
        import base64
        return base64.urlsafe_b64encode(api_key.encode()).decode()

    @staticmethod
    def from_base64(api_key):
        import base64
        return base64.urlsafe_b64decode(api_key.encode()).decode()
