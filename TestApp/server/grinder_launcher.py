# -*- coding: utf-8 -*-
# Run TestScript1 in 50% of threads, TestScript2 in 25% of threads,
# and TestScript3 in 25% of threads.
import sys
import os
import time
import logging, logging.config
from net.grinder.script.Grinder import grinder
import config
import core
from core.user import User
from core.admin import Admin
from core.exceptions import RequestFailedError
from core.exceptions import ConnectionError
from core.exceptions import InvalidArgumentError
from scripts import TestScript1
from scripts import TestScript2
from scripts import TestScript3
from scripts import TestScript4
from scripts import TestScript5

 
scripts = ["TestScript1", "TestScript2", "TestScript3"]
 
# Ensure modules are initialised in the process thread.
##or script in scripts: exec("import %s" % script)
 
def createTestRunner(script):
    exec("x = %s.TestRunner()" % script)
    return x
 
class TestRunner:
    def __init__(self):
      #  logging.config.fileConfig('logging.conf')
    #    logging.basicConfig(filename=config.LOG_FILENAME,level=logging.WARNING,)
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('main')
        tid = grinder.threadNumber
        self.testRunner = TestScript5.TestRunner()
      #  self.testRunner = TestScript1.TestRunner(tid)
     #   logging.debug('TID = %d' % tid)
       # print 'TID = ', tid
 
    #    if tid % 4 == 2:
   #         self.testRunner = createTestRunner(scripts[1])
  #      elif tid % 4 == 3:
  #          self.testRunner = createTestRunner(scripts[2])
 #       else:
  #          self.testRunner = TestScript1.TestRunner(tid)
 
    # This method is called for every run.
    def __call__(self):
        self.testRunner()


