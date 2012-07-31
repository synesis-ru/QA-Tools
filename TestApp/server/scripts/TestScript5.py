# -*- coding: utf-8 -*-
 
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
import sys
import time
import random
import urllib2
import httplib
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
test5 = Test(5, 'Game step or create session test')
logWrapper = test5.wrap(log)


 #   Тест: Игра случайного игрока. Игрок пытается сделать ход в каждой сессии из его списка сессий
 #         если сессий нет, то создается одна сессия и переходим к следующему игроку
   
class TestRunner:
       
    def __init__(self):
        """
            TestRunner constructor
            do nothing 
        """
        pass
    
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
            import traceback
            logging.warning(traceback.format_exc())
            logging.warning("***** UNCAUGHT EXCEPTION in thread %s ----description %s" % (curThreadInfo, str(e)))
            logging.warning("**********EXCEPTION INFO:\n**********THREAD - %s\n**********TYPE - %s\n**********VALUE - %s\n**********TRACEBACK - %s\n" 
                            % (curThreadInfo, sys.exc_info()[0], sys.exc_info()[1], e.__unicode__() ))
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
                conn = None
                conn = httplib.HTTPConnection(config.HTTPSERVER)
            except Exception, e:
                logging.warning("*****\n*****\n***** httplib.HTTPConnection(config.HTTPSERVER) "+ str(e))
            try:
                conn.request('GET', "")
            except Exception, e:
                logging.warning("*****\n*****\n***** conn.request('GET', "") "+ str(e))
            try:        
                response = conn.getresponse()
            except Exception, e:
                logging.warning("*****\n*****\n***** response = conn.getresponse() "+ str(e))
            try:        
                status = response.status
                if status == 200:
                    #print status
                    id = response.read()
                else:
                    if conn:
                        conn.close()
                        logging.warning("*******HTTPSERVER RESPONSE %d" % status)
                        continue
            except Exception, e:
                logging.warning("*****\n*****\n***** id = response.read() "+ str(e))   
            try:  
                conn.close()
                if id == 'EMPTY':
                    logging.warn('HTTP server gives EMPTY id')
                    continue
            except Exception, e:
                logging.warning("*****\n*****\n***** conn.close() ----------- "+ str(e))
                if conn:
                    logging.warning("conn = %s" % str(conn))
                    conn.close()
                    continue
                else:
                    logging.warning("conn = %s" % str(conn))
                    continue
            try:
                user = User(id)
                profile = user.get_or_create_profile()
               # logging.debug('Create User id = %s\n' % id )
                try:
                    user_session_list = user.get_session_list()
                except RequestFailedError:
                    logging.debug("User id = %s --- query session" % user.get_id())
                    user.query_session()
                    continue
                print 'User id = %s --- lenght session list = %d' % (user.get_id(), len(user.session_list) )
                for session in user.session_list:
                    try:
                        logging.debug(session)
                        logging.debug('++++++++++++++++++++++++++\n')
                        logging.debug("user.get_id() = %s  session.current_player_id - %s" % (user.get_id(), session.current_player_id.encode("UTF-8") ))
                        if user.get_id() == session.current_player_id.encode("UTF-8"):
                            user.update_session(session, 'A' * 25) #25600
                    except RequestFailedError, err_rfe:
                        logging.warning('UPDATE SESSION-----------RequestFailedError!-----------\n'+ str(err_rfe))
                        continue
                    except Exception, e:
                        logging.warning("***** GET  RESPONSE ERROR "+ str(e))
                        continue
                        
            except RequestFailedError, err_rfe:     
               # print '-----------RequestFailedError!-----------\n'+err_rfe
                pass
            except ConnectionError, err_ce:
                logging.warning( '-----------ConnectionError!-----------\n'+ str(err_ce))
                continue
            except InvalidArgumentError, err_ia:
                logging.warning( '-----------InvalidArgumentError!-----------\n'+ str(err_ia))
                continue
        logging.debug('---------------------------TEST 2 IS PASSED------------------------')       
    
 
