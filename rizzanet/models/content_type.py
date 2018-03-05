from sqlalchemy import Column,String,Integer,ForeignKey,PickleType
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base,db_session

class ContentType(Base):
    '''Defines content types'''
    __tablename__ = 'ContentType'
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True)
    schema = Column(PickleType)
    def __init__(self,name,schema):
        self.name = name
        self.schema = schema
    def verify(self,data):
        for name,datatype in self.schema.items():
            if not name in data.keys():
                print('Error: verification for item {0} failed due to {1} not being present in passed data.'.format(self.name,name))
                return False
            if type(data[name]) != datatype:
                print('Error: verification failed for item {0} due to attribute {1} not matching in type with schema {2} != {3}.'.format(self.name,name,type(data[name]),datatype))
                return False
        return True
    @classmethod 
    def create(self,name,schema):
        '''Creates a new content type'''
        content_type = self(name,schema)
        db_session.add(content_type)
        db_session.commit()
        return content_type