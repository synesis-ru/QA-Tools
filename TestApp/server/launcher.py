#!/usr/bin/jython 
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import httplib
import simplejson as json
import logging, logging.config 
import unittest
import time
import config
from tests.servertests import ServerTests 
from core.user import User
from core.admin import Admin
from core.exceptions import RequestFailedError
from core.exceptions import ConnectionError
from core.exceptions import InvalidArgumentError


def suite():   
    return unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(ServerTests()) )
    
def main():
    '''
        Тест: Игра двух конкретных игроков.
        1 - Игрок1 рисует;
        2 - Игрок2 угадывает;
        3 - Игрок2 рисует;
    '''
    try:
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('main')
        user1 = User('1003')
        user2 = User('1004')
        u2_list = user2.get_session_list()
        u1_list = user1.get_session_list()
        print "user is=%s lenght session list = %d" % (user2.get_id(), len(user2.get_session_list()))
        for session in u2_list:
            print session
            print "-------------"
            user2.update_session(session, 'A' * 25)
            session = user2.get_session(session.id)
            logging.debug(session)
            user1.update_session(session, 'A' * 25)
            session = user2.get_session(session.id)
            logging.debug(session)
            user1.update_session(session, 'A' * 25)
            session = user2.get_session(session.id)
   
    except RequestFailedError, err_rfe:   
        print '-----------RequestFailedError!-----------' 
    except ConnectionError:
        print '-----------ConnectionError!-----------'
    except InvalidArgumentError:
        print '-----------InvalidArgumentError!-----------'
  
  
  
  
  
  
def main546():
    '''
        Тест: Игра случайного игрока. Игрок пытается сделать ход в каждой сессии из его списка сессий
    '''
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('main')
    while True:
        try:
           # resp = urllib2.urlopen('http://localhost:8000')
            
            conn = None
            conn = httplib.HTTPConnection('localhost:8000')
            conn.request('GET', "")
            response = conn.getresponse()
            status = response.status
            print status
            id = response.read()
            conn.close()
            if id == 'EMPTY':
                logging.warn('HTTP server gives EMPTY id')
                continue
            
           # id = resp.read()
          #  resp.close()
           # if id == 'EMPTY':
           #     logging.warn('HTTP server gives EMPTY id')
           #     break
            user = User(id)
            logging.debug('Create User id = %s\n' % id )
            quantity_sessions = len(user.session_list)
            logging.debug('user quantity sessions = %d' % quantity_sessions)
            user.query_session()
            time.sleep(5)
            user_session_list = user.get_session_list()
            logging.debug('!!!user quantity sessions = %d' % len(user.session_list))
            if len(user.session_list) == 0:
                continue
            else:
                for session in user.session_list:
                    try:
                        logging.debug(session)
                        logging.debug('++++++++++++++++++++++++++\n')
                        user.update_session(session, 'Test_URL')
                    except RequestFailedError:
                        print 'UPDATE SESSION-----------RequestFailedError!-----------'
                        continue
            #break
        except RequestFailedError:     
            print '-----------RequestFailedError!-----------'
        except ConnectionError:
            print '-----------ConnectionError!-----------'
        except InvalidArgumentError:
            print '-----------InvalidArgumentError!-----------'
        except Exception, e:
                logging.warning("*****\n*****\n***** GET HTTPSERVER RESPONSE "+ str(e))
                if conn:
                    logging.warning("conn = %s" % str(conn))
                    conn.close()
                    continue
                else:
                    logging.warning("conn = %s" % str(conn))
                    continue
    logging.debug('TEST IS PASSED')
    
            
    
def main56():
  #  logging.config.fileConfig('logging.conf')
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('main')
    admin = Admin()
    for i in range(1000005, 1000008):
        try:
            admin.create_user(str(i))
        except RequestFailedError:
            logging.info(u'Create user %d - RequestFailedError\n' % i)
            continue
    

if __name__ == '__main__':
    main()
    
 #   unittest.main()
 
