from .basetype import BaseType

class ImageType(BaseType):
    '''stringtype for rizzanet'''
    type_name = 'image'
    @classmethod
    def verify(cls, instance):
        from io import BytesIO
        from PIL import Image
        import base64
        try:
            image_data = cls.get_image_data(instance)
            Image.open(BytesIO(base64.b64decode(image_data)))
            return True
        except Exception:
            return False
    
    @staticmethod 
    def get_image_data(data):
        import re
        return  re.sub('^data:image/.+;base64,', '', data)
    
    @staticmethod
    def get(data):
        from rizzanet.models import ImageData
        print(ImageData.get_by_hash(data))
        return ImageData.get_by_hash(data)

    @staticmethod
    def get_es_value(data):
        return data

    @staticmethod
    def after_validation_convert(data):
        from rizzanet.events import dispatchEvent
        import hashlib
        data = ImageType.get_image_data(data)
        if isinstance(data, str):
            data = data.encode()
        
        image_hash = hashlib.md5(data).hexdigest()
        dispatchEvent('CREATE_IMAGE', image_hash, data)
        return image_hash

