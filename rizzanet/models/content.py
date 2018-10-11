from sqlalchemy import Column,String,Integer,Text,ForeignKey,Boolean,exists,and_
from sqlalchemy.orm import relationship,backref
from rizzanet.db import Base
from rizzanet.events import dispatchEvent
from .content_data import ContentData
from .content_type import ContentType
from hashlib import md5
from flask import render_template,render_template_string,g

class Content(Base):
    '''Main content object for site'''
    __tablename__ = 'Content'
    id = Column(Integer,primary_key=True)
    parent_id = Column(Integer, ForeignKey('Content.id'))
    name = Column(String(255))
    path = Column(Text)
    remote_id = Column(String(128),unique=True)
    main_node = Column(Boolean)
    content_type_id = Column(Integer,ForeignKey('ContentType.id'))
    content_type = relationship('ContentType', uselist=False)
    content_data_id = Column(Integer,ForeignKey('ContentData.id'))
    content_data = relationship('ContentData', uselist=False)

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
        self.main_node = None
        self.main_node = self.is_main_node()
        self.remote_id = self.get_remote_id()
        self.path = self.get_full_path()

    def __repr__(self):
        return '<Content({0})>'.format(','.join([str(name)+':'+str(value) for name, value in self.as_dict().items()]))
        
    def as_dict(self):
        return dict(
            id = self.id,
            name = self.name,
            remote_id = self.remote_id,
            parent_id  = self.parent_id,
            content_data_id = self.content_data_id,
            path = self.path,
            main_node = self.main_node
        )

    def is_main_node(self):
        if self.main_node != None:
            return self.main_node
        nodes = ContentData.get_by_id(self.content_data_id).get_nodes()
        # Assume that if any other nodes exist this node is null 
        return len(nodes) == 0
    
    def get_main_node(self):
        return self.get_content_data().get_main_node()

    def regenerate_path_tree(self):
        '''Rebuilds hash tree for child nodes of this tree'''
        self.remote_id = self.get_remote_id()
        self.node = self.get_full_path()
        for child in self.get_children():
            child.regenerate_path_tree()
        self.refresh()

    def get_remote_id(self):
        return md5(self.get_full_path().strip('/').encode()).hexdigest()

    def get_children(self):
        '''Gets children of a given node'''
        return g.db_session.query(Content).filter(Content.parent_id==self.id).all()

    def get_subtree(self,**kwargs):
        children = self.get_children()
        as_dict = kwargs.get('as_dict',False)
        with_content_objects = kwargs.get('with_content', False)
        depth = kwargs.get('depth', -1)
        
        if depth > 0:
            kwargs['depth'] -= 1

        subtrees = [child.get_subtree(**kwargs) for child in children]
        self.children = children
        if as_dict:
            to_return = self.as_dict()
            if with_content_objects:
                to_return = {**self.get_content_data().as_dict(),**to_return}
            if self.children == [] or depth == 0:
                return to_return
            to_return['children'] = subtrees
            return to_return
        return self

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
            return g.db_session.query(Content).get(self.parent_id)

    def get_globals(self):
        '''Gets globals to inject into context of jinja template on self.render() call'''
        return dict(
            node = self,
            content = self.content_data
        )

    def get_template_context(self):
        '''Gets context for a template render'''
        return {**self.content_data.get_data(),**self.get_globals()}

    def get_id(self):
        return self.id

    def render(self):
        '''renders a content location'''
        from rizzanet.core.render import get_render_service
        render_service = get_render_service()
        return render_service.render(self)

    def add_child(self,name,content_data_id,content_type_id=None):
        '''Adds and commits a new child into the database'''
        if content_type_id == None: content_type_id = content_data_id
        content_type_id = ContentType.get_content_type_from_mixed(content_type_id).get_id()
        new_node = Content(self.id, name, content_type_id, content_data_id)
        g.db_session.add(new_node)
        g.db_session.flush()
        g.db_session.refresh(new_node)
        dispatchEvent('CREATE_CONTENT', new_node)
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
        g.db_session.flush()
        return self

    def get_content_data(self):
        '''Gets content data'''
        return self.content_data
    
    def get_content_type(self):
        '''gets content data'''
        return self.content_type

    def get_path(self):
        return self.path

    def refresh(self):
        g.db_session.add(self)
        g.db_session.flush()
        g.db_session.refresh(self)
        return self

    def set_as_main_node(self):
        if self.main_node:
            return True
        old_node = self.get_main_node()
        old_node.main_node = False
        self.main_node = True
        old_node.refresh()
        self.refresh()
        return True



    @classmethod
    def get_by_remote_id(self,remote_id):
        '''gets class by remote id'''
        return g.db_session.query(self).filter(self.remote_id==remote_id).first()

    @classmethod
    def get_by_path(self,path):
        '''gets class by full path'''
        return self.get_by_remote_id(md5(path.strip('/').encode()).hexdigest())

    @classmethod
    def get_by_id(self,id):
        '''Gets content by id'''
        return g.db_session.query(self).filter(self.id==id).first()

    @classmethod
    def get_by_ids(cls, ids):
        return g.db_session.query(cls).filter(cls.id._in(ids)).all()

    @classmethod
    def get_by_content_data(cls, data):
        if isinstance(data, ContentData):
            data = data.id
        return g.db_session.query(cls).filter(cls.content_data_id == data).all()

    @classmethod
    def get_main_by_content_data(cls, data):
        if isinstance(data, ContentData):
            data = data.id
        return g.db_session.query(cls).filter(and_(cls.content_data_id == data, cls.main_node)).one()

    @classmethod
    def exsists(cls, content_id):
        return g.db_session.query(exists().where(cls.id == content_id)).scalar()  
    
    @classmethod 
    def create(cls,parent_id, name, content_type_id, content_data_id):
        node=Content(parent_id, name, ContentType.get_content_type_from_mixed(content_type_id).get_id(), content_data_id)
        g.db_session.add(node)
        g.db_session.flush()
        dispatchEvent('CREATE_CONTENT', node)
        return node

    @classmethod
    def all(cls, batch=10):
        '''Returns a genarator that iterates through all instances of this type'''
        import math
        for contentlist in (g.db_session.query(cls).limit(batch).offset(batch*x).all() for x in range(0,math.ceil(g.db_session.query(cls).count()/batch))):
            for content in contentlist:
                yield content