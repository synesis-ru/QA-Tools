# -*- coding: utf-8 -*-
class Session():
        
    def __init__(self, params): 
        """
            Arguments: params -- dictionary
            init session
        """
        self.id = params[u'id']
        self.version = params[u'version']
        self.current_player_id = params[u'cur_player']
        self.waiting_player_id = params[u'wait_player']
        self.closed = params[u'closed']
        self.action = params[u'action']
        self.draw = params[u'draw']
        self.quess = params[u'guess']
        self.old_draw = params[u'old_draw']
        
    def __str__(self):
        """
            Convert session object to string
            Return string
        """
        
        str_id =  'Id = %s\n' % self.id
        str_version = 'Version = %d\n' % self.version
        str_current_player_id = 'CurrentPlayerId = %s\n' % self.current_player_id
        str_waiting_player_id = 'WaitingPlayerId = %s\n' % self.waiting_player_id
        str_closed = 'closed = %s\n' % self.closed
        str_action = 'Action = %s\n' % self.action
        str_draw = 'Draw = %s\n' % self.draw
        str_quess = 'Quess = %s\n'% self.quess
        str_olddraw = 'Old draw = %s\n'% self.old_draw
        result = str_id + str_version + str_current_player_id + \
                 str_waiting_player_id + str_closed + str_action + \
                 str_draw + str_quess + str_olddraw
        return result  
            
