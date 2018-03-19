from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base,db_session
from .content_data import ContentData
from .content_type import ContentType
from hashlib import md5
from flask import render_template

class Content(Base):
    '''Main content object for site'''
    __tablename__ = 'Content'
    id=Column(Integer,primary_key=True)
    parent_id = Column(Integer, ForeignKey('Content.id'))
    name=Column(String(255))
    remote_id=Column(String(128),unique=True)
    content_type_id=Column(Integer,ForeignKey('ContentType.id'))
    content_type=relationship('ContentType', uselist=False)
    content_data_id=Column(Integer,ForeignKey('ContentData.id'))
    content_data=relationship('ContentData', uselist=False)

    def __init__(self, parent_id, name, content_type_id, content_data_id):
        if isinstance(parent_id,Content):
            self.parent_id=parent_id.id
        else:
            self.parent_id = parent_id
        if isinstance(content_data_id,ContentData):
            self.content_data_id = content_data_id.id
        else:
            self.content_data_id  = content_data_id
        if isinstance(content_type_id,ContentType):
            self.content_type_id = content_type_id.id
        else:
            self.content_type_id  = content_type_id
        self.name = name
        self.remote_id = ''
        self.regenarate_remote_id()

    def __repr__(self):
        return '<Content(id:{0},parent_id:{1},name:{2},content_type_id:{3},content_data_id:{4})>'.format(self.id,self.parent_id,self.name,self.content_type_id,self.content_data_id)

    def regenarate_remote_id(self):
        '''Rebuilds hash tree for child nodes of this tree'''
        self.remote_id=md5(self.get_full_path().strip('/').encode()).hexdigest()
        for child in self.get_children():
            child.regenarate_remote_id()

    def get_children(self):
        '''Gets children of a given node'''
        return db_session.query(Content).filter(Content.parent_id==self.id).all()

    def get_full_path(self):
        '''gets full path of content object'''
        parent=self.get_parent()
        if parent == None:
            return ''
        return parent.get_full_path()+'/'+self.name

    def get_parent(self):
        '''gets parent node of a given node (if root node returns None)'''
        if self.parent_id==None:
            return None
        else:
            return Content.query.get(self.parent_id)

    def render(self):
        '''renders a content location'''
        return render_template(self.content_type.get_view_path(),**self.content_data.get_data())

    def add_child(self,name,content_data_id,content_type_id=None):
        '''Adds and commits a new child into the database'''
        if content_type_id == None: content_type_id = content_data_id
        content_type_id = ContentType.get_content_type_from_mixed(content_type_id).get_id()
        new_node = Content(self.id, name, content_type_id, content_data_id)
        db_session.add(new_node)
        db_session.flush()
        return new_node

    def check_circular(self, stack=[]):
        '''Checks for circular references in content tree'''
        stack.push(self.id)
        if self.parent_id == '':
            return True
        if self.parent_id in stack:
            return False
        return self.get_parent().check_circular(stack)

    def move(self, new_parent):
        if isinstance(new_parent,Content):
            new_parent_id = new_parent.id
        else:
            new_parent_id = new_parent
        if self.check_circular([new_parent_id]):
            return False
        self.parent_id=new_parent_id
        db_session.flush()
        return self

    def get_content_data(self):
        '''Gets content data'''
        return ContentData.get_by_id(self.content_data_id)

    @classmethod
    def get_by_remote_id(self,remote_id):
        '''gets class by remote id'''
        return db_session.query(self).filter(self.remote_id==remote_id).first()
    @classmethod
    def get_by_path(self,path):
        '''gets class by full path'''
        return self.get_by_remote_id(md5(path.strip('/').encode()).hexdigest())

    @classmethod
    def get_by_id(self,id):
        '''Gets content by id'''
        return db_session.query(self).filter(self.id==id).first()
            
        