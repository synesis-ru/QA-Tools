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
test2 = Test(2, 'Game step test')
logWrapper = test2.wrap(log)


 #   Тест: Игра случайного игрока. Игрок пытается сделать ход в каждой сессии из его списка сессий
   
class TestRunner:
       
    def __init__(self):
        """
            TestRunner constructor
            do nothing 
        """
        pass
      #  grinder.logger.info('Thread #%d started' % grinder.threadNumber )
    
    def __call__(self):
        """
            run  __test_call__ method
        """
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
        """
            random player trying to do step 
            in each session in his session list
        """
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('main')
        sec = random.randrange(1,5)
        time.sleep(sec)
        while True:
            try:
                resp = urllib2.urlopen(config.HTTPSERVER)
                id = resp.read()
                resp.close()
                if id == 'EMPTY':
                    logging.warn('HTTP server gives EMPTY id')
                    break
            except urllib2.HTTPError, exception:
                resp.close()
                logging.info('*****\n*****\n***** GET HTTPSERVER RESPONSE------HTTP error %d' % exception.code)
                continue
            except urllib2.URLError, exception:
                resp.close()
                logging.info("*****\n*****\n***** GET HTTPSERVER RESPONSE -----------URLError: %s" % exception.reason.args[1])
                resp = ''
                continue
            except Exception, e:
                resp.close()
                logging.warning("*****\n*****\n***** GET HTTPSERVER RESPONSE "+ str(e))
                continue
            try:
                user = User(id)
                logging.debug('Create User id = %s\n' % id )
                user.query_session()
               # sec = random.randrange(1,5)
                time.sleep(2)
                user_session_list = user.get_session_list()
                quantity_sessions = len(user.session_list)
                while len(user.session_list) == 0:
                    time.sleep(2)
                    user_session_list = user.get_session_list()
                print 'User id = %s --- lenght session list = %d' % (user.get_id(), len(user.session_list) )
                while len(user.session_list) < 10:
                    quantity_sessions = len(user.session_list)
                    user.query_session()
                    while len(user.session_list) != (quantity_sessions +1):
                        logging.debug('user id = %s ---- len(user.session_list) = %d ---- quantity_sessions = %d\n' 
                                      %(user.get_id(), len(user.session_list), quantity_sessions))
                        time.sleep(4)
                        user_session_list = user.get_session_list()
#                    logging.debug('User id = %s --- lenght session list = %d' % (user.get_id(), quantity_sessions ))
                logging.debug('user quantity sessions = %d' % quantity_sessions)
        #        user_session_list = user.get_session_list()
                logging.debug('!!!user quantity sessions = %d' % len(user.session_list))
             #  if len(user.session_list) == 0:
             #      continue
                for session in user.session_list:
                    try:
                        logging.debug(session)
                        logging.debug('++++++++++++++++++++++++++\n')
                        logging.debug("user.get_id() = %s  session.current_player_id - %s" % (user.get_id(), session.current_player_id.encode("UTF-8") ))
                        if user.get_id() == session.current_player_id.encode("UTF-8"):
                            user.update_session(session, 'A' * 25600)
                    except RequestFailedError, err_rfe:
                        print 'UPDATE SESSION-----------RequestFailedError!-----------\n'+err_rfe
                        continue
                    except ConnectionError, err_ce:
                        print '-----------ConnectionError!-----------\n'+err_ce
                        continue
                    except InvalidArgumentError, err_ia:
                        print '-----------InvalidArgumentError!-----------\n'+err_ia
                        continue 
                    except Exception, e:
                        logging.warning("***** GET  RESPONSE ERROR "+e)
                        sys.exit(-1)
                        
            except RequestFailedError, err_rfe:     
               # print '-----------RequestFailedError!-----------\n'+err_rfe
                pass
            except ConnectionError, err_ce:
                print '-----------ConnectionError!-----------\n'+err_ce
                continue
            except InvalidArgumentError, err_ia:
                print '-----------InvalidArgumentError!-----------\n'+err_ia
                continue
        logging.debug('---------------------------TEST 2 IS PASSED------------------------')       
    
 
