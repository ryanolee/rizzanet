from sqlalchemy import Column,String,Integer,ForeignKey,PickleType,exists
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base
from flask import g
from .content_type import ContentType
from rizzanet.events import dispatchEvent
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
    
    def __repr__(self):
        return '<ContentData({0})>'.format(','.join(['{0!s}:{1!r}'.format(key, obj) for key, obj in self.as_dict().items()]))
    
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
    
    def get_data_dict(self):
        return self.data

    def get_datatype(self):
        return self.datatype

    def get_datatype_id(self):
        return self.datatype_id

    def get_datatype_object(self):
        return ContentType.get_by_id(self.datatype_id)

    def update(self, data={}, **kwargs):
        for key, value in {**data, **kwargs}.items():
            self.update_attr(key, value)

    def update_attr(self, name ,data):
        from rizzanet.fieldtypes.valueobject import ValueObject
        from .content_type import ContentType
        content_type = ContentType.get_by_id(self.datatype_id)
        schema = content_type.get_schema()
        if not name in schema:
            raise ValueError('Name {0} not in schema for {1}'.format(name, self.get_datatype)) 
        attr = schema['name']
        if isinstance(data, ValueObject):
            data = data.get()
        self.data['name'] = ValueObject(data, attr)
        g.db_session.add(self)
        g.db_session.flush()
        g.db_session.refresh(self)
        dispatchEvent('UPDATE_CONTENT_DATA', self)
        return self
            
    
    def get_main_node(self):
        from .content import Content
        return Content.get_main_by_content_data(self.id)

    def get_attr(self, name):
        if not name in self.data:
            raise ValueError('Attribute {0!s} not in content data {1!r}'.format(name, self ))
        target = self.data[name]
        target.bind_content_data(self)
        return target
    
    def get_attr_map(self):
        return {name: value.bind_content_data(self) for name, value in self.data.items()}

    def get_nodes(self):
        from .content import Content
        return Content.get_by_content_data(self.id)

    def get_id(self):
        return self.id

    @classmethod 
    def create(cls,name,data):
        if isinstance(name,ContentType):
            schema=name.schema
            name=name.name
        else:
            schema = ContentType.get_by_name(name)
        types = schema.get_schema()
        data = {key: types[key].create(data[key] if key in data else None) for key in types.keys()}
        if not schema.verify(data):
            return None
        #Create value objects from the related content types 
        content_data = cls(name,data)
        g.db_session.add(content_data)
        g.db_session.flush()
        g.db_session.refresh(content_data)
        dispatchEvent('CREATE_CONTENT_DATA', content_data)
        return content_data
    
    @classmethod
    def get_by_id(cls, data_id):
        try:
            content_data = g.db_session.query(cls).filter( cls.id ==  data_id).one()
        except Exception as error:
            raise Exception('Error no content data found with id:{0} error: {1}'.format( data_id,error))
        return content_data

    @classmethod
    def get_by_ids(cls, ids):
        return g.db_session.query(cls).filter(cls.id.in_(ids)).all()
    
    @classmethod
    def exsists(cls, data_id):
        return g.db_session.query(exists().where(cls.id == data_id)).scalar()
    
    @classmethod
    def all(cls, content_type, batch=10):
        '''Returns a genarator that iterates through all instances of this type'''
        import math
        content_type = ContentType.get_content_type_from_mixed(content_type)
        for content_data_list in (g.db_session.query(cls).filter(cls.datatype_id == content_type.id).limit(batch).offset(batch*x).all() for x in range(0,math.ceil(g.db_session.query(cls).count()/batch))):
            for content_data in content_data_list:
                yield content_data
            
        