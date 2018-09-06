
class ImageHelper:

    ALLOWED_FILTERS = ['convert', 'crop', 'alpha_composite', 'quantize', 'resize', 'remap_palette', 'rotate', 'transform', 'transpose']
    NON_RETURNING_FILTERS = ['thumbnail']

    def __init__(self, app):
        self.image_path = app.static_folder + app.config['IMAGES']['PATH'].strip('/')+'/'
        self.image_url_path = app.static_url_path +'/' + app.config['IMAGES']['PATH'].strip('/')+'/'
        self.allowed_types = app.config['IMAGES']['ALLOWED_FORMATS']
        self.aliases = app.config['IMAGES']['ALIASES']
        self.force_convert = app.config['IMAGES']['FORCE_CONVERT']
        self.default_format = app.config['IMAGES']['DEFAULT_FORMAT']
        self.default_alias_name = app.config['IMAGES']['DEFAULT_ALIAS']
        self.auto_dump = app.config['IMAGES']['DEFAULT_ALIAS']
        self.verbose = False

    def set_verbose(self,verbose):
        self.verbose = bool(verbose)

    def dump_images(self, verbose = False):
        from rizzanet.models import ImageData
        
        import os

        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)

        for image in ImageData.all():
            image_object = image.get_image_object()
            name = image.get_name()
            self.dump_image(name, image_object)
            

    def dump_image(self, name, image):
        from PIL import Image
        from copy import deepcopy
        if not isinstance(image, Image.Image):
            raise ValueError('Error: Unexpected image passed to the ImageHelper.image_dump method expected:' + str(Image)  + ' Got:' + str(type(image)))
        if not image.format.lower() in self.allowed_types:
            if self.verbose: print('Warning image not an allowed format: image format {0} not in allowed types: {1}'.format(image.format, ','.join(self.allowed_types))) 
            if self.force_convert:
                #Commit in memory file conversion if format of image file not allowed
                from io import BytesIO
                with BytesIO as buffer:
                    image.save(buffer, format=self.default_format)
                    buffer.seek(0)
                    image = Image.open(buffer)
        image_format = image.format
        print(image_format)
        for alias_name, alias_data in self.aliases.items():
            target = deepcopy(image)
            target = self.apply_alias(target, alias_data)
            
            if self.verbose: print('Saving image: {0!s}_{1!s}'.format(name, alias_name))
            self.save_image(target, name, alias_name, image_format)
    
    def apply_alias(self, image, alias):
        from PIL import Image
        if not isinstance(image, Image.Image):
            raise ValueError('Error: Unexpected image passed to the Image.dump_image_for_alias method expected:' + image.__class__ + ' Got:' + type(image))
        for filter_layer in alias:
            image = self.apply_filter(image, filter_layer)
        return image
    
    def apply_filter(self, image, filter_layer):
        from PIL import Image
        filter_data = filter_layer['args'] if 'args' in filter_layer else {}
        if not 'filter' in filter_layer:
            self._raise_warning('No filter applied in call to {0!s}.apply_filter()'.format(str(type(self))))
            return image
        filter_name = filter_layer['filter']
        if not filter_name in self.ALLOWED_FILTERS:
            self._raise_warning('Filter not allowed in call to {0!s}.apply_filter(). Filter {1!s} must be one of {2!s}'.format(str(type(self)), filter_layer['filter'], self.ALLOWED_FILTERS))
            return image
        if not hasattr(image, filter_layer['filter']):
            raise RuntimeError('Error: filter {0!s} is not an attribute of the {1!s} class.')
        filter_method = getattr(image, filter_name)
        if not callable(filter_method):
            raise RuntimeError('Error: filter {0!s} is not an valid method of .')
        try:
            #Return result of applied image filter
            res = filter_method(**filter_data)
            if self.verbose: print('Applying filter: {0!r}'.format(filter_method))
            return image if filter_name in self.NON_RETURNING_FILTERS else res
        except Exception as e:
            self._raise_warning('Exception thrown while executing filter: {0!s} filter not applied!'.format(e))
            return image
            

    def _raise_warning(self, warning_str):
        import warnings
        if self.verbose: print(warning_str)
        warnings.warn(warning_str, RuntimeWarning)
        return False
    
    def get_image_path(self, name, alias, image_format):
        return self.image_path + name + '_' + alias + '.' + image_format.lower()

    def save_image(self, image, name, alias_name, image_format='', **kwargs):
        if image.format != None and image_format == '':
            image_format = image.format
        image_path = self.get_image_path(name, alias_name, image_format)
        if self.verbose: print('Saving image: {0}'.format(image_path))
        image.save(image_path, **kwargs)

    def get_image_uri(self, image, alias=None):
        from rizzanet.models import ImageData
        import os
        if not isinstance(image, ImageData):
            raise ValueError('Error: cannot get URI for non ImageData object expected {0} got {1}'.format(ImageData.__name__, str(type(image))))
        if alias == None:
            alias = self.default_alias_name
        image_name = image.get_name()
        image_format = image.get_format()
        image_path = self.get_image_path( image_name, alias, image_format)
        if os.path.exists(image_path):
            return self.image_url_path + image_name + '_' +alias + '.' + image_format
        alias_data = self.get_alias_data_by_name(alias)
        image = self.apply_alias(image.get_image_object(), alias_data)
        if self.auto_dump: self.save_image(image, image_name, alias, image_format)
        return self.get_data_uri_from_image(image, image_format)
    
    def get_data_uri_from_image(self, image, image_format):
        from io import BytesIO
        from base64 import b64encode
        #@todo possible url safe base 64 encode?
        buffered = BytesIO()
        image.save(buffered, format=image_format)
        img_str = b64encode(buffered.getvalue()).decode()
        return 'data:{0};base64,{1}'.format(image_format, img_str)

    def get_alias_data_by_name(self, name):
        if not name in self.aliases:
            self._raise_warning('Warning: Image alias {0} not in alias {1}'.format(name, ','.join([str(key) for key in self.aliases.keys()])))
            return []
        return self.aliases[name]
        