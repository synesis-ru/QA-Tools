# -*- coding: utf-8 -*-

class StorageObject():
    """
        Class which describes location where put object
    """
    def __init__(self, params):
        """
            Arguments: params -- dictionary
            init storageobject
        """
        self.location = params[u'location']
        self.key = params[u'key']
        
    def to_dict(self):
        """
            Convert StorageObject object to dictionary
            Return dictionary
        """
        return {u'location': self.location, u'key': self.key}
    