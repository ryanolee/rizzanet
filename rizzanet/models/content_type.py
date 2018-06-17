from sqlalchemy import Column,String,Integer,ForeignKey,PickleType,exists
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base
from flask import g

class ContentType(Base):
    '''Defines content types'''
    __tablename__ = 'ContentType'
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True)
    schema = Column(PickleType)
    view_path = Column(String(255))

    def __init__(self,name,schema,view_path=''):
        from rizzanet.fieldtypes import BaseType
        self.name = name
        for item in schema.values():
            if not issubclass(item, BaseType):
                raise Exception('Error while creating content type: {0!r} does not inherit from BaseType'.format(item))
        self.schema = schema
        self.view_path = view_path

    def as_dict(self):
        return dict(
            id = self.id,
            name = self.name,
            schema = self.get_schema_as_dict(),
            view_path = self.view_path
        )

    def verify(self,data):
        for name,datatype in self.schema.items():
            if not name in data.keys():
                print('Error: verification for item {0} failed due to {1} not being present in passed data.'.format(self.name,name))
                return False
            if datatype.verify(data[name]):
                print('Error: verification failed for item {0} due to attribute {1} not matching in type with schema {2} != {3}.'.format(self.name,name,type(data[name]),datatype))
                return False
        return True

    def get_schema_as_dict(self):
        return {key : val.get_type_name() for key, val in self.schema.items()}

    def get_schema(self):
        return self.schema

    def get_view_path(self):
        return self.view_path

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    @classmethod 
    def create(cls,name,schema,view_path=''):
        '''Creates a new content type'''
        content_type = cls(name,schema,view_path)
        g.db_session.add(content_type)
        g.db_session.flush()
        g.db_session.refresh(content_type)
        return content_type
    
    @classmethod
    def get_content_type_from_mixed(cls, content_type):
        '''gets a content type from a mixed value
        Args:
            content_type (mixed): Retrievs a content type from a mixed value
                Case: string -> Gets content type from name
                Case: ContentType -> Returns passed content type
                Case: ContentData -> Returns associated content type
                Case: Int -> Int assumed to be ID and returns content type by ID
                Default: Returns None
        Returns:
            ContentType
        '''
        from .content_data import ContentData
        if isinstance(content_type,str):
            return ContentType.get_by_name(content_type)
        elif isinstance(content_type,ContentType):
            return content_type
        elif isinstance(content_type,int):
            return cls.get_by_id(content_type)
        elif isinstance(content_type,ContentData):
            return cls.get_by_id(content_type.get_datatype_id())
        else:
            return None
    
    @classmethod
    def get_by_id(cls, type_id):
        try:
            content_type_id = g.db_session.query(cls).filter( cls.id ==  type_id).one()
        except Exception as error:
            raise Exception('Error no content class found with id:{0} error: {1}'.format( type_id,error))
        return content_type_id

    @classmethod 
    def get_by_name(cls, name):
        try:
            content_type = g.db_session.query(cls).filter(name==cls.name).one()
        except Exception as error:
            raise Exception('Error no content class found with name:{0} error: {1}'.format(name,error))
        return content_type
    
    @classmethod
    def exsists(cls, type_id):
        return g.db_session.query(exists().where(cls.id == type_id)).scalar()

    @classmethod
    def all(cls, batch=10):
        '''Returns a genarator that iterates through all instances of this type'''
        import math
        return (g.db_session.query(cls).limit(batch).offset(batch*x) for x in range(0,math.ceil(g.db_session.query(cls).count()/batch)))