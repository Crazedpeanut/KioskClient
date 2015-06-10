'''
Author: John Kendall
Date: 18/12/14

Description: Logging script to display debug messages on in the standard output or to record them in a file
'''

import datetime
import os
import time
import settings
from inspect import currentframe, getframeinfo

DEBUGGING = settings.DEBUGGING
DEBUGGING_MODE = settings.DEBUGGING_MODE
PRINT_DATETIME = settings.PRINT_DATETIME
PRINT_FRAME_INFO = settings.PRINT_FRAME_INFO
debugging_active = False

def debug(message):
    global debugging_active

    if(DEBUGGING == True):
        dbugmsg = "DEBUG: " + message
        
        if(PRINT_FRAME_INFO):
            frameinfo = currentframe()
            filename = getframeinfo(frameinfo.f_back).filename
            
            dbugmsg += " | Filename: " + filename
            dbugmsg += " | Line Num: " + str(frameinfo.f_back.f_lineno)

        if(PRINT_DATETIME == True):
            current_time = datetime.datetime.now()
            dbugmsg += " | " + str(current_time)
           
        
        while(debugging_active == True):
            time.sleep(0.5)
        
        dbugmsg += "\n\n\n"

        try:
            debugging_active = True

            if(DEBUGGING_MODE == 1):
                print(dbugmsg)
            elif(DEBUGGING_MODE == 2):
                if(os.path.isfile("debug.log")):
                    f = open("debug.log", "a")
                    f.write(dbugmsg)
                else:
                    f = open("debug.log", "w")
                    f.write(dbugmsg)
        except Exception as e:
            print(str(e))
        finally:
            debugging_active = False
