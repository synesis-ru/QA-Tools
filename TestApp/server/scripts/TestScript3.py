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
test3 = Test(3, 'all users are playing ')
logWrapper = test3.wrap(log)

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
                    break
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
                session_list = user.get_session_list()
                quantity_sessions = len(user.session_list)
                logging.info("user id = %s len(user.session_list = %d)" % (user.get_id, quantity_sessions))
                if quantity_sessions < 1:
                    continue
                else:
                    for session in user.session_list:
                        try:
                            logging.debug(session)
                            logging.debug('++++++++++++++++++++++++++\n')
                            logging.debug("user.get_id() = %s  session.current_player_id - %s" % (user.get_id(), session.current_player_id.encode("UTF-8") ))
                            if user.get_id() == session.current_player_id.encode("UTF-8"):
                                user.update_session(session, 'A' * 25600)
                        except RequestFailedError, err_rfe:
                            logging.warning('UPDATE SESSION-----------RequestFailedError!-----------\n' + str(err_rfe))
                            continue
                        except ConnectionError, err_ce:
                            logging.warning('-----------ConnectionError!-----------\n' + str(err_ce))
                            continue
                        except InvalidArgumentError, err_ia:
                            logging.warning('-----------InvalidArgumentError!-----------\n' + str(err_ia))
                            continue 
                        except Exception, e:
                            logging.warning("***** GET  RESPONSE ERROR " + str(e))
                            continue
            except RequestFailedError, err_rfe:     
                pass
            except ConnectionError, err_ce:
                logging.warning( '-----------ConnectionError!-----------\n'+ str(err_ce))
                continue
            except InvalidArgumentError, err_ia:
                logging.warning( '-----------InvalidArgumentError!-----------\n'+ str(err_ia))
                continue
        logging.info('---------------------------TEST 4 IS PASSED------------------------')       
    
 
