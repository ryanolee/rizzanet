from sqlalchemy import Column,String,Integer,ForeignKey,PickleType,exists
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base
from flask import g
from .content_type import ContentType
class ContentData(Base):
    '''Defines content types'''
    __tablename__ = 'ContentData'
    id = Column(Integer,primary_key=True)
    datatype_id = Column(Integer,ForeignKey('ContentType.id'))
    datatype = Column(String(255))
    data = Column(PickleType)

    def __init__(self,datatype,data):
        self.datatype = datatype
        self.data = data
        self.datatype_id = ContentType.get_content_type_from_mixed(datatype).get_id()
    
    def as_dict(self):
        return dict(
            id = self.id,
            data_type = self.get_datatype(),
            data_type_id = self.get_datatype_id(),
            data = self.get_data()
        )
        
    def get_data(self):
        return {key: value.get() for key,value in self.data.items()}

    def set_data(self, data):
        self.data = data

    def get_datatype(self):
        return self.datatype

    def get_datatype_id(self):
        return self.datatype_id

    @classmethod 
    def create(self,name,data):
        if isinstance(name,ContentType):
            schema=name.schema
            name=name.name
        else:
            schema = ContentType.get_by_name(name)
        types = schema.get_schema()
        data = {key: types[key].create(data[key] if key in data else None) for key in types.keys()}
        if schema.verify(data):
            #Create value objects from the related content types 
            content_data = ContentData(name,data)
            g.db_session.add(content_data)
            g.db_session.flush()
            g.db_session.refresh(content_data)
            return content_data
        else:
            return None
    
    @classmethod
    def get_by_id(cls, data_id):
        try:
            content_data = g.db_session.query(cls).filter( cls.id ==  data_id).one()
        except Exception as error:
            raise Exception('Error no content data found with id:{0} error: {1}'.format( data_id,error))
        return content_data
    
    @classmethod
    def exsists(cls, data_id):
        return g.db_session.query(exists().where(cls.id == data_id)).scalar()
    
    @classmethod
    def all(cls, content_type, batch=10):
        '''Returns a genarator that iterates through all instances of this type'''
        import math
        content_type = ContentType.get_content_type_from_mixed(content_type)
        return (g.db_session.query(cls).filter(cls.datatype_id == content_type.id).limit(batch).offset(batch*x) for x in range(0,math.ceil(g.db_session.query(cls).count()/batch)))
            
        