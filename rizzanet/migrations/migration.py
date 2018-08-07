
class Migration:
    def __init__(self,file,verbose=False):
        self.file = file
        self.state={}
        self.verbose=verbose
        self._id_mappings={}
        self._content_mappings={}

    def load(self):
        from yaml import safe_load
        from jsonschema import validate
        from .migration_schema import MIGRATION_SCHEMA
        import os
        pathname = os.path.join(os.path.dirname(__file__),self.file)
        if self.verbose: print("Loading migration from {0} ...".format(pathname))
        if not os.path.exists(pathname):
            raise FileNotFoundError('Error file not found at point {0}'.format(pathname))
        with open(pathname,'r') as file:
           state = safe_load(file)
        #validate(state,MIGRATION_SCHEMA)
        self.state = state
        
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
                self._content_mappings[name] = ContentData.create(data['type'],data['data'])
                
        if 'content' in self.state:
            for name, data in self.state['content'].items():
                if self.verbose: print("Creating content node {0}".format(name))
                content_node = Content.create(
                    None if not 'id' in data else data['id'],
                    data['name'] if 'name' in data else name,
                    data['type'],
                    self.create_data_object(
                        data['type'],
                        data['data'],
                ))
                if 'label' in data:
                    self._content_mappings[data['label']] = content_node 
                self.build_content_struct(
                    content_node
                    ,data['children']
                )
    '''For internal use only'''
    def build_content_struct(self ,root_node, data):
        if data == None:
            return
        for key,value in data.items():
            if self.verbose: print("Creating content node {0}".format(key))
            data_type = None if not 'type' in value else value['type']
            content_data = self.handle_content_data_substitution(value['data'])
            content_data = self.create_data_object(data_type, content_data)
            node = root_node.add_child(key, content_data, data_type)

            if 'label' in value:
                self._content_mappings[value['label']] = node 
            self.build_content_struct(node, value['children'] if 'children' in value else None)
        
    def create_data_object(self, datatype, data, label=None):
        from rizzanet.models import ContentData
        if isinstance(data, str):
            if not data in self._id_mappings:
                raise KeyError('Error no mapping to content data '+data+' found')
            # Get content data based of id key mappings
            if self.verbose: print('Loading content data as it already exsists.')
            content_data = ContentData.get_by_id(self._id_mappings[data])
        else:
            if self.verbose: print('Creating content data with type {0}'.format(datatype))
            content_data = ContentData.create(datatype,data)
        if label != None: 
            self._content_mappings[label] = content_data
        return content_data
        
    def handle_content_data_substitution(self, content_data):
        import re
        if isinstance(content_data, str):
            offset = 0
            for hit in re.compile("\${(\w+)\.?(\w*)}").finditer(content_data):
                if self.verbose: print('Interpolating value:'+ hit.group(0))
                #Uses group 1 for name of content data. Skip if the content data is found
                if not hit.group(1) in self._content_mappings:
                    continue
                target_data = self._content_mappings[hit.group(1)]
                #Return full content data if attribute is not defiend
                if hit.group(2) == '':
                    return target_data
                if hasattr(target_data, hit.group(2)):
                    target_value =  getattr(target_data, hit.group(2))
                    content_data = content_data[0:hit.start()+offset] + str(target_value) + content_data[hit.end()+offset:]
                    #update offset for change in stinglength made by replacement
                    offset += len(str(target_value)) - (hit.end() - hit.start()) 
            return content_data
        elif isinstance(content_data, list):
            return [self.handle_content_data_substitution(cd) for cd in content_data]
        elif isinstance(content_data, dict):
            return {name:  self.handle_content_data_substitution(cd) for name, cd in content_data.items()}
        return content_data