# -*- coding: utf-8 -*-
import sys
import simplejson as json
import logging
import urllib
import exceptions
import session as Session
import requests
from storageobject import StorageObject
from gamestep import GameStep
  
class User:
    
    def __init__(self, id):
        self.id = id
        self.sessionlist_version = 0
        self.token = '1'
        self.current_session = None
        self.session_list = []
       # self.exchange_token() # will be work at the next week
        
    def get_id(self):
        return self.id   
    
    def get_session_list_version(self):
        return self.sessionlist_version
    
    def exchange_token(self):
        request = '/auth/exchange_token?' + urllib.urlencode({'socialnetwork' : config.SOCIAL_NETWORK, 'token': config.TOKEN}, 'user_id' : self.id})
        decoded = requests.do_get_request(request)
        if decoded:
            self.token = decoded[u'object']
        else:
            raise exceptions.RequestFailedError(decoded)(decoded)
      
    def put_object(self, params):
        try:
            request = '/object/put?' + urllib.urlencode({'token': self.token})
         #   print "request = %s" % request
            decoded = requests.do_post_request(request, params)
            print "PUT OBJECT DECODED =%s" % decoded
            logging.debug(str(decoded[u'object']))
            if decoded:
                storageobject = StorageObject(decoded[u'object'])
                return storageobject
            else:
                logging.warn("---put object is fail---\n")
        except  exceptions.RequestFailedError, e:
            logging.warn("put_object %s --------RequestFailedError-----------%s " % (self.id, e))
    
    def update_session(self, session, obj):
        try:
            logging.debug('-------update session-------\n%s' % session)
            request = '/session/update?' + urllib.urlencode({'token': self.token})
            step_obj = self.put_object(obj)
            game_step = GameStep(self.id, session, step_obj)
            encoded = json.dumps(game_step.to_dict())
            logging.debug('\n--encoded game step--\n%s' % encoded)
            decoded = requests.do_post_request(request, encoded)
            print "GAME STEP DECODED =%s " % decoded
            if decoded:
                res_session = Session.Session(decoded[u'object'])
                logging.debug('\n+++++++++++++++++++++Update session for user id =%s is OK!!!!\n'  % self.id)
                self.current_session = res_session
               # return res_session
            else:
                logging.warn('Update session for user id =%s is fail\n' % self.id)
        except  exceptions.RequestFailedError, e:
            logging.warn("update_session %s --------RequestFailedError-----------%s " % (self.id, e))
           # raise exceptions.RequestFailedError(decoded)
            
        
        
    def get_profile(self):
        '''
            Get profile dictionary          
        '''
        try:
            profile = {}
            request = '/user/get?' + urllib.urlencode({'token': self.token, 'user_id': self.id})
            decoded = requests.do_get_request(request)    
            if decoded:
                profile = decoded[u'object']
                return profile
        except  exceptions.RequestFailedError, e:
            logging.warn("get_profile %s --------RequestFailedError-----------%s " % (self.id, e))

    def get_or_create_profile(self):
        '''
            Get or create profile dictionary          
        '''
        try:
            profile = {}
            request = '/user/get_or_create?' + urllib.urlencode({'token': self.token, 'user_id': self.id })
            decoded = requests.do_get_request(request)    
            if decoded:
                profile = decoded[u'object']
                logging.debug("User is = %s was created" % self.get_id())
                return profile
        except  exceptions.RequestFailedError, e:
            logging.warn("get_or_create_profile %s --------RequestFailedError-----------%s " % (self.id, e))
    
    def get_friends(self):
        pass
     
    def query_session(self):
        ''' 
            OK
            Create game session query for user,
            Note: When server has 2 session query from different users 
            it create game session
        '''
        try:
            request = '/session/query?' + urllib.urlencode({'token': self.token, 'user_id': self.id })
            decoded = requests.do_get_request(request)
            if decoded:
                logging.debug('query session for User = %s is OK' % self.id)
            else:
               logging.warning("Query error!!!!") 
          #S  raise exceptions.RequestFailedError(decoded)
        except  exceptions.RequestFailedError, e:
            logging.warn("query_session %s --------RequestFailedError-----------%s " % (self.id, e))
                   
    def get_session_list(self):
        '''
            OK
        '''
    #    logging.debug('session list version = %d ' % self.sessionlist_version)
        request = '/session/list/get?' + urllib.urlencode({'token' : self.token, 'user_id' :  self.id, 'version' : self.sessionlist_version})
        print request
        session_list = []
        decoded = requests.do_get_request(request)  
        if decoded:
            self.sessionlist_version = decoded[u'object'][u'version']
            for item in decoded[u'object'][u'sessions']:
                session = Session.Session(item)
                session_list.append(session)   
                self.session_list.append(session)  
        return session_list
     
    def close_session(self, session_id):
        ''' 
            OK
            Delete session from current user session list.
            Note: This session in opponent session list is marked as "closed"
            When opponent makes CloseSession() for this session, 
            session will be deleted from server
        '''
        try:
            request = '/session/close?' +  urllib.urlencode({'token' : self.token, 'user_id' :  self.id, 'session_id' : session_id})
            decoded = requests.do_get_request(request)
            if decoded:
                pass
        except  exceptions.RequestFailedError, e:
            logging.warn("close session %s --------RequestFailedError-----------%s " % (session_id, e))
            
    def get_session(self, session_id):
        '''
            Return session
        '''
        try:
            request = '/session/get?' + urllib.urlencode({'token' : self.token, 'session_id' : session_id})
            decoded = requests.do_get_request(request)
            if decoded:
                self.current_session = Session.Session(decoded[u'object'])
                return self.current_session
        except  exceptions.RequestFailedError, e:
            logging.warn("get_session %s --------RequestFailedError-----------%s " % (session_id, e))
            