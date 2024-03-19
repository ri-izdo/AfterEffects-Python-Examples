'''Execute AEKeyFramestoMotion task.
'''
import os
import sys
import json
import csv
import subprocess

SCRIPTS = os.path.abspath("")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import AE_configuration as config
import AE_keyframe_converter as keyframe_converter

# counter = 0
# for arg in sys.argv:
#     print(f"sys.argv[{counter}]: {sys.argv[counter]}")
#     counter += 1

try:
    TASKLIST_FILE = sys.argv[1]
    NUMBERS_TO_CSV_SCRIPT = sys.argv[2]
    TASK_LIST_CSV = sys.argv[3]
    SCRIPTS_DIR = sys.argv[4]
except ValueError:
    print("Error: AE_Tasklist.py constants required.")

def tasklist(func):
    def wrapper(*args, **kwargs):        
        scpt = str(args[0])
        csv_file = str(args[2])

        p = subprocess.Popen(
                ['/usr/bin/osascript', scpt], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = p.communicate()
        p.terminate()
        config.close_app(args[1])

        return csv_file
                
    return wrapper


@tasklist
def generate_task_list(*args, **kwargs):
    return args

def open_tasklist_file():
    '''Open Numbers.app and tasklist.
    '''
    open_file = f"{str(TASKLIST_FILE)}"
    try:
        cmd = [
            "open",
            open_file
        ]
        subprocess.call(cmd)
        # value = input("Fill in the task list and DO NOT close application. Press Return to continue...")
        print(".\n.\n.\n.")
        result = input("Press [1] to execute task list: ")
    except:
        print("Error: Tasklist file.")
        print(f"Task List file path: {TASKLIST_FILE}")
        value = input("Return any key to exit.")
        config.kill_ppid()

    if result == "1":
        print("Execute admin module.")
        try:
            csv_file = generate_task_list(
                NUMBERS_TO_CSV_SCRIPT,
                "Numbers",
                TASK_LIST_CSV
            )
            exist = os.path.exists(csv_file)

            return csv_file
        except ValueError:
            print("Error: Injecting task list")
    else:
        print("Result not [1].")

def new_node_keyframe_converter():
    '''Create a new node and initiate a task list.
    '''
    # Install required tools.
    converter_script = os.path.join(SCRIPTS_DIR, "AE_keyframe_converter.py")
    cmd_arguments = f"{converter_script} {TASK_LIST_CSV}"

    try:
        config.new_node(cmd_arguments)
    except ValueError:
        print("Error: Task list node.")

if __name__ == '__main__':
    try:
        csv_file = open_tasklist_file()
        print(f"csv_file: {csv_file}")
        new_node_keyframe_converter()
        config.kill_ppid()

    except ValueError:
        print("Error: AE_tasklist.py")
