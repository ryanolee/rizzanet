
from sqlalchemy import Column,String,Integer,LargeBinary
from sqlalchemy.orm import relationship,backref,deferred
from rizzanet.db import Base
from rizzanet.events import attachEventListener
from flask import g


class ImageData(Base):
    __tablename__ = 'ImageData'
    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    image_hash = Column(String(32))
    data = deferred(Column(LargeBinary))
    image_format = Column(String(10))
    def __init__(self, name, data):
        import hashlib
        img = self._image_data_to_object(data)
        
        self.image_format = img.format.lower()
        self.name = name
        if isinstance(data, str):
            data = data.encode()
        self.image_hash = hashlib.md5(data).hexdigest()
        self.data = data

    def get_image_object(self):
        return self._image_data_to_object(self.data)

    def get_name(self):
        return self.name
    
    def get_format(self):
        return self.image_format
    
    def as_dict(self):
        return dict(
            name = self.name,
            image_hash = self.image_hash,
            image_format = self.image_format
        )
    

    @classmethod
    def create(cls, name, data):
        image = cls(name, data)
        g.db_session.add(image)
        g.db_session.flush()
        return image

    @classmethod
    def all(cls, batch=10):
        '''Returns a genarator that iterates through all instances of this type'''
        import math
        for imagelist in (g.db_session.query(cls).limit(batch).offset(batch*x).all() for x in range(0,math.ceil(g.db_session.query(cls).count()/batch))):
            for content in imagelist:
                yield content

    @classmethod
    def get_by_hash(cls, image_hash):
        return g.db_session.query(cls).filter(cls.image_hash==image_hash).one()

    @staticmethod
    def _image_data_to_object(img_data):
        from io import BytesIO
        from PIL import Image
        from base64 import b64decode
        return Image.open(BytesIO(b64decode(img_data)))


attachEventListener('CREATE_IMAGE', ImageData.create)