
# -*- coding: utf-8 -*-
from storageobject import StorageObject

class GameStep():
    
    def __init__(self, id, session, stepdata):
        self.user_id = id
        self.session_id = session.id
        self.version = session.version
      #  self.action = action
        self.stepdata = stepdata
        self.word = 'TESTWORD'
        self.isguess = None
        self.points = 3
        if session.action == 'draw':
            self.action = 'guess'
        else:
            self.action = 'draw'
        
    def to_dict(self):
        '''
            Return object dictionary
        '''
        return {u'session_id': self.session_id, u'user_id': self.user_id, 
                u'version': self.version,u'action': self.action,
                u'stepdata': self.stepdata.to_dict()}#, u'word': self.word,
              #  u'isguess': self.isguess, u'points': self.points}
        
