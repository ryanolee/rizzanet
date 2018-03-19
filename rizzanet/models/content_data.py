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
        self.datatype_id = ContentType.get_content_type_from_mixed(datatype).get_id()
    def get_data(self):
        return self.data

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
        if schema.verify(data):
            content_data = ContentData(name,data)
            db_session.add(content_data)
            db_session.flush()
            return content_data
        else:
            return None
    
    @classmethod
    def get_by_id(self, data_id):
        try:
            content_data = db_session.query(self).filter( self.id ==  data_id).one()
        except Exception as error:
            raise Exception('Error no content data found with id:{0} error: {1}'.format( data_id,error))
        return content_data
            
        