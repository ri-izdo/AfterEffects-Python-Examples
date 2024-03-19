'''Execute AEKeyFramestoMotion task.
'''
import os
import sys
import subprocess

SCRIPTS = os.path.abspath("")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import AE_configuration as config

TASKLIST_FILE = os.path.join(os.path.abspath("../data"),"task_list.numbers")
NUMBERS_TO_CSV_SCRIPT = os.path.join(os.path.abspath(""), "numbers_to_csv.scpt")
TASK_LIST_CSV = os.path.join(os.path.expanduser('~'), "Documents/task_list.csv")

def check_tools():
    '''Make sure tools exists.
    '''
    try:
        inspect_setup = config.inspect_setup()
    except ValueError:
        print("Error: Checking tools.")

def new_node_tasklist():
    '''Create a new node and initiate a task list.
    '''
    # Install required tools.
    cmd_arguments = f"AE_tasklist.py {TASKLIST_FILE} {NUMBERS_TO_CSV_SCRIPT} {TASK_LIST_CSV} {SCRIPTS}"

    try:
        config.new_node(cmd_arguments)
    except ValueError:
        print("Error: Task list node.")


if __name__ == '__main__':
    check_tools()
    new_node_tasklist()
