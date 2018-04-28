
class Migration:
    def __init__(self,file,verbose=False):
        self.file = file
        self.state={}
        self.verbose=verbose
        self._id_mappings={}

    def load(self):
        from yaml import safe_load
        import os
        pathname = os.path.join(os.path.dirname(__file__),self.file)
        if self.verbose: print("Loading migration from {0} ...".format(pathname))
        if not os.path.exists(pathname):
            raise FileNotFoundError('Error file not found at point {0}'.format(pathname))
        with open(pathname,'r') as file:
            self.state = safe_load(file) 
    
    def commit(self):
        from rizzanet.models import Content,ContentData,ContentType
        from rizzanet.fieldtypes.alltype import CLASS_MAPPINGS
        self._id_mappings = {}
        if 'content_type' in self.state:
            for name, data in self.state['content_type'].items():
                if self.verbose: print("Creating content type {0}".format(name))
                new_data = ContentType.create(name,{key: CLASS_MAPPINGS[value] for key, value in data['schema'].items()},data['view_path'] if 'view_path' in data else None)
                self._id_mappings[name] = new_data.id
        if 'content_data' in self.state:
            for name, data in self.state['content_data'].items():
                if self.verbose: print("Creating content data {0}".format(name))
                ContentData.create(data['type'],data)
        if 'content' in self.state:
            for name, data in self.state['content'].items():
                if self.verbose: print("Creating content node {0}".format(name))
                self.build_content_struct(
                    Content.create(
                        None if not 'id' in data else data['id'],
                        data['name'] if 'name' in data else name,
                        data['type'],
                        self.create_data_object(data['type'],data['data']))
                    ,data
                )
    '''For inturnal use only'''
    def build_content_struct(self ,root_node, data):
        if data == None:
            return
        for key,value in data['children'].items():
            if self.verbose: print("Creating content node {0}".format(key))
            data_type = None if not 'type' in value else value['type']
            node = root_node.add_child(key,self.create_data_object(data_type, data['data']), data_type)
            self.build_content_struct(node, value['children'] if 'children' in value else None)
        
    def create_data_object(self, datatype, data):
        from rizzanet.models import ContentData
        if isinstance(data, str):
            if not data in self._id_mappings:
                raise KeyError('Error no mapping to content data '+data+' found')
            # Get content data based of id key mappings
            if self.verbose: print('Loading content data as it already exsists.')
            return ContentData.get_by_id(self._id_mappings[data])
        else:
            if self.verbose: print('Creating content data with type {0}'.format(datatype))
            return ContentData.create(datatype,data)
        

        
        