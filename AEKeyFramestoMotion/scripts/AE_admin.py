'''Delegate paths and paramaters. 
To be used to scale multiple tasks.
'''
'''Execute AEKeyFramestoMotion task.
'''
import os
import sys
import json
import subprocess
import csv

SCRIPTS = os.path.abspath("")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import AE_configuration as config
import AE_interpolator as interpolator

# def tasklist(func):
#     def wrapper(*args, **kwargs):        
#         scpt = config.applescript(str(args[0]))
        
#         p = subprocess.Popen(
#                 ['/usr/bin/osascript', scpt], 
#                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         out, err = p.communicate()
#         p.terminate()
#         config.close_app(args[1])

#     return wrapper


# @tasklist
# def generate_task_list(*args, **kwargs):
#     return args
