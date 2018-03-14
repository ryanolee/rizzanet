from sqlalchemy import Column,String,Integer,ForeignKey,PickleType
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base,db_session
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
    def get_data(self):
        return self.data
    def set_data(self, data):
        self.data = data
    def get_datatype(self):
        return self.datatype
    @classmethod 
    def create(self,name,data):
        if isinstance(name,ContentType):
            schema=name.schema
            name=name.name
        else:
            try:
                schema=db_session.query(ContentType).filter(name==ContentType.name).one()
            except Exception as error:
                raise Exception('Error no content class {0} found:{1}'.format(name,error))
        if schema.verify(data):
            content_data = ContentData(name,data)
            db_session.add(content_data)
            db_session.commit()
            return content_data
        else:
            return None
        
            
        