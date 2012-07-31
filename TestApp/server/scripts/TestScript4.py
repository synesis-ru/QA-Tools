# -*- coding: utf-8 -*-
 
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
import sys
import time
import random
import urllib2
import logging, logging.config
import config
from core.user import User 
from core.session import Session
from core.admin import Admin
from core.exceptions import RequestFailedError
from core.exceptions import ConnectionError
from core.exceptions import InvalidArgumentError
import java
 
log = grinder.logger.info
test4 = Test(4, 'Creating 10 sessions for each user')
logWrapper = test4.wrap(log)

 #   Тест: Создание по 10 сессий для каждого игрока
   
class TestRunner:
       
    def __init__(self):
        pass
      #  grinder.logger.info('Thread #%d started' % grinder.threadNumber )
    
    def __call__(self):
       # logging.basicConfig(level=logging.DEBUG)
       # log = logging.getLogger('main')
        curThreadInfo = java.lang.Thread.currentThread().toString()
        try:
            logging.debug("******* Staring task %s" % curThreadInfo)
            self.__test_call__()
            logging.debug("******* Finished task %s" % curThreadInfo)
        except Exception, e:
            logging.warning("***** UNCAUGHT EXCEPTION in thread %s ----description %s" % (curThreadInfo, str(e)))
            logging.warning("**********EXCEPTION INFO:\n**********THREAD - %s\n**********TYPE - %s\n**********VALUE - %s\n**********TRACEBACK - %s\n" 
                            % (curThreadInfo, sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]) )
            sys.exit(-1)
    
    def __test_call__(self):
        sec = random.randrange(1, 7)
        time.sleep(sec)
        while True:
            try:
                resp = None
                resp = urllib2.urlopen(config.HTTPSERVER)
                id = resp.read()
                resp.close()
                if id == 'EMPTY':
                    logging.warning('HTTP server gives EMPTY id')
                   # break
                    continue # if one of httpservers send EMPTY, test continue working with other httpservers
            except urllib2.HTTPError, exception:
                logging.warning('*****\n*****\n***** GET HTTPSERVER RESPONSE------HTTP error %d' % exception.code)
                if resp:
                    logging.warning("resp = %s" % resp)
                    resp.close()
                    continue
                else:
                    logging.warning("resp = %s" % resp)
                    continue
            except urllib2.URLError, exception:
                logging.warning("*****\n*****\n***** GET HTTPSERVER RESPONSE -----------URLError: %s" % exception.reason.args[1])
                if resp:
                    logging.warning("resp = %s" % resp)
                    resp.close()
                    continue
                else:
                    logging.warning("resp = %s" % resp)
                    continue
            except Exception, e:
                logging.warning("*****\n*****\n***** GET HTTPSERVER RESPONSE "+ str(e))
                if resp:
                    logging.warning("resp = %s" % resp)
                    resp.close()
                    continue
                else:
                    logging.warning("resp = %s" % resp)
                    continue
          #      sys.exit(-1)
            try:
                user = User(id)
                logging.debug('Create User id = %s\n' % id )
                user.query_session()
                sec = random.randrange(3, 7)
                time.sleep(sec)
                user_session_list = user.get_session_list()
                quantity_sessions = len(user.session_list)
                while len(user.session_list) == 0:
                    sec = random.randrange(3, 7)
                    time.sleep(sec)
                    user_session_list = user.get_session_list()
                print 'User id = %s --- lenght session list = %d' % (user.get_id(), len(user.session_list) )
                while len(user.session_list) < 10:
                    quantity_sessions = len(user.session_list)
                    user.query_session()
                    while quantity_sessions >= len(user.session_list):
                        logging.debug('user id = %s ---- len(user.session_list) = %d ---- quantity_sessions = %d\n' 
                                      %(user.get_id(), len(user.session_list), quantity_sessions))
                        time.sleep(4)
                        user_session_list = user.get_session_list()
                    logging.debug("user id =%s session list is incremented!!!" % user.get_id())
                logging.debug('!!!user quantity sessions = %d' % len(user.session_list))
            except RequestFailedError, err_rfe:     
                pass
            except ConnectionError, err_ce:
                logging.warning( '-----------ConnectionError!-----------\n'+ str(err_ce))
                continue
            except InvalidArgumentError, err_ia:
                logging.warning( '-----------InvalidArgumentError!-----------\n'+ str(err_ia))
                continue
        logging.info('---------------------------TEST 4 IS PASSED------------------------')       
    
 
