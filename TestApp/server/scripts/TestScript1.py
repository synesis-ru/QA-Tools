# -*- coding: utf-8 -*-
 

from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
import sys
import time
import logging, logging.config
import config
from core.user import User 
from core.session import Session
from core.admin import Admin
from core.exceptions import RequestFailedError
from core.exceptions import ConnectionError
from core.exceptions import InvalidArgumentError
 
 
log = grinder.logger.info
test1 = Test(1, "Creating 1000000 users")
logWrapper = test1.wrap(log)


class TestRunner:
 
    def __init__(self, tid):
        self.tid = tid
        
    def __call__(self):
      #  for 10 threads
        logWrapper("TestScript1")
        admin = Admin()
        try:
            for i in range(0, 100000):
                id = i + (self.tid-1) * 100000
                admin.create_user(str(id))
                
        except RequestFailedError:
            logWrapper(u'Create user %d - RequestFailedError\n' % id)
            logging.warn((u'Create user %d - RequestFailedError\n' % id))
        
      #  for i in range(1010, 1015):
      #      try:
      #          admin.create_user(str(i))
      #      except RequestFailedError:
      #          logWrapper(u'Create user %d - RequestFailedError\n' % i)
      #          continue
    


