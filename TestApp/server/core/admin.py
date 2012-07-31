
# -*- coding: utf-8 -*-

import sys
import urllib2
import logging
import config
import requests
import exceptions


class Admin():
    
    def __init__(self):
        self.name = 'Admin'
        
    def get_alphabet(self):
        request = 'game/data?token=%s&id=alphabet' %token
        resp = urllib2.urlopen(config.SERVER + request)
        data = resp.read()
        resp.close()
    
    def create_user(self, id):
        logging.debug('----create user  %s------' % id)
      #  print '----create user  %s------' % id
        request = 'user/create?token=%s&user_id=%s' % (config.TOKEN, id)
        decoded = requests.do_get_request(request)
    #    logging.debug('decoded = %s' % decoded)
        if decoded:
            pass
         #   print 'User %s was created' % id
           # logging.debug('User %s was created' % id)
        else:
          #  print 'User %s wasn\'t created' % id
           #logging.debug('User %s wasn\'t created' %id)
            print 'User %s wasn\'t created' %id
            raise exceptions.RequestFailedError
       
