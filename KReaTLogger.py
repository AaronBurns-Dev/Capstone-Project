#!/usr/bin/python
"""
Author: Praveen Rai
Date: 03/14/2019

Module sets logging to both file and console
"""

#IMPORTS
import logging
import os.path
import datetime
import threading

#GLOBALS
LOG_FILE_PATH = "./"
TASK_LIST = {}

class KREATLog(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.logHandle = None
                self.logFormatter = None
                self.handler = None
                self.fileName = None

                self.fileName = self.getUniqueFilename()
                self.logHandle = logging.getLogger(__name__)
                self.logHandle.setLevel(logging.DEBUG)
                self.logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

                # create debug file handler and set level to debug
                self.handler = logging.FileHandler(os.path.join(LOG_FILE_PATH, self.fileName),"a+")
                self.handler.setFormatter(self.logFormatter)
                self.logHandle.addHandler(self.handler)

                # create console handler
                self.handler = logging.StreamHandler()
                self.handler.setFormatter(self.logFormatter)
                self.logHandle.addHandler(self.handler)

        def dumpMsg(self, msg):
                self.logHandle.debug(msg)

        def getUniqueFilename(self):
                lclStr = datetime.datetime.now().strftime("%Y_%m_%d")+str("_RunLog.log")
                return(lclStr)		


def KREATDEBUG(msg):
        global TASK_LIST
        key = __name__
        logger = None
        loggerPresent = False
        #print (TASK_LIST)        
        try:
                if(len (TASK_LIST) > 0):
                        if(key in TASK_LIST):
                                logger = TASK_LIST[key]
                                loggerPresent = True
                if(loggerPresent == False):
                        logger = KREATLog()
                        TASK_LIST.update({key:logger})
                        
                logger.dumpMsg(msg)
        except:
                print("Logging me an exception")


if __name__ == '__main__':
        KREATDEBUG("This is test called from logger main function")       
