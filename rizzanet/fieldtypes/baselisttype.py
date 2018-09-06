from .basetype import BaseType
from abc import abstractmethod
class BaseListType(BaseType):

    item_type = None 

    '''Base list type for all iterable types'''
    @classmethod
    def verify(cls, instances):
        '''Validates all instances of a list type against it's respective list type'''
        #fail if class passed is invalid
        if not issubclass(cls.item_type,BaseType):
            raise TypeError('Class {0} does not inherit from BaseType'.format(cls.item_type))
        #Check if passed instance is iterable 
        try:
            iter(instances)
        except TypeError:
            return False
        instances = [cls.item_type.convert(instance) for instance in instances]
        return all([cls.verify_item(instance) for instance in instances])

    @classmethod
    def convert(cls, instances):
        '''converts a number of instances in tandem'''
        return [cls.item_type.convert(instance) for instance in instances]

    @classmethod
    def after_validation_convert(cls,instances):
        '''converts a number of instances in tandem'''
        return [cls.item_type.after_validation_convert(instance) for instance in instances]


    @classmethod
    def get_item(cls, item):
        '''Default value for return item'''
        return cls.item_type.get(item)
    
    @classmethod
    def set_item(cls, item):
        '''defines the transformation to apply to items before storing them'''
        return cls.item_type.set(item)

    @classmethod
    def verify_item(cls, instance):
        '''Default to no validation for list items'''
        return cls.item_type.verify(instance)
        