# -*- coding: utf-8 -*-
import sys

class RequestFailedError(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


class ConnectionError(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
     
     
class InvalidArgumentError(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        str_value = str(self.value)
        return str_value