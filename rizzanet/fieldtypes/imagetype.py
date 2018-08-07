from .basetype import BaseType

class ImageType(BaseType):
    '''stringtype for rizzanet'''
    type_name = 'image'
    @classmethod
    def verify(cls, instance):
        from io import BytesIO
        from PIL import Image
        import base64
        image_data = cls.get_image_data(instance)
        try:
            Image.open(BytesIO(base64.b64decode(image_data)))
            return True
        except Exception:
            return False
    
    @staticmethod 
    def get_image_data(data):
        import re
        return  re.sub('^data:image/.+;base64,', '', data)