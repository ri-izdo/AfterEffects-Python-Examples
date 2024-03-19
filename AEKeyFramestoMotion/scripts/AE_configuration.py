'''Configure overall task.
'''

import os
import sys
import subprocess
import signal

def install_pip():
    '''Install Python's standard package manager.
    '''
    cmd = [
        "curl",
        "https://bootstrap.pypa.io/get-pip.py",
        "-o",
        "get-pip.py"
    ]
    py_cmd = [
        "python3",
        "get-pip.py"
    ]
    exit_cmd = [
        "rm",
        "get-pip.py"
    ]

    cmd_list = [cmd, py_cmd, exit_cmd]

    for c in cmd_list:
        subprocess.call(c)

def install_tools():
    '''Install tools required for AEKeyFramestoMotion script.
    '''
    try:
        path = os.path.join(os.path.abspath(""),"requirements.txt")
    except:
        print("Could not build path.")
    cmd = [
        "pip",
        "install",
        "-r",
        str(path)
    ]
    subprocess.call(cmd)

def update_python():
    cmd = [
        "python",
        "-m",
        "pip",
        "install",
        "--upgrade",
        "setup",
        "tools"
    ]
    cmd_list = [py_version, cmd]
    try:
        for c in cmd_list:
            subprocess.call(c)
    except:
        print("Could not update python")

def inspect_setup():
    '''Install required tools. Source list in required.txt
    Prequisite:
    applescript
    pyperclip
    '''
    subprocess_tools = 0
    
    while subprocess_tools <= 0:
        print("Check tool prerequisites.")
        try:
            import applescript
            import pyperclip
            import pandas
            subprocess_tools += 1
        except:
            try:
                install_pip()
                install_tools()
                subprocess_tools += 1
            except:
                print("Sufficient tools required.")
    tool_requirements = True

    return tool_requirements

def applescript(applescript_file):
    try:
        return applescript_file
    except KeyError:
        raise ValueError('Needs an apple script name. Refer to: /scpt path')


###
# . Ingest and require
###
'''Require Motion file and AEKey 
1. Check all formats are correct
2. 
3.
'''

###
# . Import target file 
###

###
# . Parse data
###
'''
'''

###
# . Generate header string
###

###
# . Store string
###

##########################################################
#
# Basic config commands for terminal use.
# 
##########################################################


def exp_user():
    # Home path.
    return os.path.expanduser('~')


def kill_ppid():
    '''Close terminal
    '''
    ppid = os.getppid()
    print(ppid)
    return os.kill(ppid, signal.SIGHUP)

def close_app(app_name):
    cmd = [
        "killall",
        str(app_name)
    ]
    return subprocess.call(cmd)
    

def data_path():
    path = os.path.join(os.path.abspath("../.."),"data")
    return path


def new_node(*args, **kwargs):
    try:
        print("Start new node.")
        import applescript
        script = args[0]
        python_script = os.path.join(os.path.abspath(""),args[0])
        applescript.tell.app(f"Terminal", f'do script "python3 {python_script}"')
    except ValueError:
        print("Error: Start new node.")

    
##########################################################
#
# Temp Data Configuration
# 
##########################################################

def func_temp_data(func):
    '''This function creates and deletes temp data.
    '''
    def wrapper(*args, **kwargs):
        print("Creating temp data.")
        mode = args[0]
        project = args[1]
        temp_loader("start", project)
    return wrapper

@func_temp_data
def temp_data(*args, **kwargs):
    return args, kwargs

def temp_loader(mode, project):
    if mode == "start":
        temp_dir_generator(1, project)
    if mode == "end":
        temp_dir_generator(2, project)

def temp_dir_generator(mode, project):
    path = os.path.join(exp_user(),f"Documents/{project}_temp_data")
    exists = os.path.exists(path)
    cmd_rm = [
        "rm",
        "-r",
        str(path)
    ]
    cmd_mk = [
        "mkdir",
        str(path)
    ]
    if mode == 1:
        if exists == True:
            subprocess.call(cmd_rm)
            print("Deleting temp data")
            pass
        return subprocess.call(cmd_mk)
    if mode == 2:
        return subprocess.call(cmd_rm)

########################################################################
#
#
# Temporary data: use for input output infratructure.
#
#
########################################################################

def generate_temp_data(TEMP_DIRPATH):
    print(f'Created temp folder here: {TEMP_DIRPATH}')
    try:
        return os.mkdir(TEMP_DIRPATH)
    except:
        shutil.rmtree(TEMP_DIRPATH)
        print("A temp directory already exists, I will need to delete that to proceed.")
        print("Recreating temp directory.")
        return os.mkdir(TEMP_DIRPATH)

def create_tmp_folder(TEMP_DIRPATH):
    print(TEMP_DIRPATH)
    try:
        return os.mkdir(TEMP_DIRPATH)
    except:
        shutil.rmtree(TEMP_DIRPATH)
        print("A temp directory already exists, I will need to delete that to proceed.")
        print("Recreating temp directory.")
        return os.mkdir(TEMP_DIRPATH)   


def remove_tmp_folder(TEMP_DIRPATH):
    cmd = [
        'sudo',
        'rm',
        '-r',
        str(TEMP_DIRPATH)
    ]
    return subprocess.call(cmd)

def cp_media_image(path_to_hitArea_image, TEMP_DIRPATH):
    print(f"copying media image: {path_to_hitArea_image}")
    cp_cmd = [
        'cp',
        path_to_hitArea_image,
        TEMP_DIRPATH
    ]
    subprocess.call(cp_cmd)


def make_json_config(path_to_added_posterFrame, TEMP_DIRPATH):
    '''Make json config for path directories to be used for generating art.
    '''
    print("Writing temp file.")
    path_to_txt_config = os.path.join(TEMP_DIRPATH + '/config.txt')
    txt_config = str(path_to_added_posterFrame)

    try:
        '''
        with open(path_to_json_config, 'w') as outfile:
            json.dump(json_config, outfile)
        print(f"Create JSON config: {path_to_json_config}")
        '''
        print("Writing temp file")
        with open(path_to_txt_config, 'w') as txtfile:
            txtfile.write(txt_config)

    except:
        print(f"Could not write json file to: {path_to_txt_config}")
        pass


def remove_photoshop_scripts(TEMP_VERT_COORDS, jsx_file, photoshop_startupScripts_dir, TEMP_DIRPATH):
    jsx_file = os.path.join(photoshop_startupScripts_dir,jsx_file)
    del_jsx_cmd = [
        "sudo",
        "rm",
        str(jsx_file)
    ]

    rm_vert_cmd = [
        "sudo",
        "rm",
        TEMP_VERT_COORDS
        ]
    try: 
        subprocess.call(del_jsx_cmd)
        shutil.rmtree(TEMP_DIRPATH)
        print("Deleted temp_data files.")
    except:
        pass

    try:
        subprocess.call(rm_vert_cmd)
    except:
        pass


def processing(total_seconds):

    animation = "|/-\\"
    idx = 0

    # String to be displayed when the application is loading 
    load_str = f"Processing."
    ls_len = len(load_str) 
  
  
    # String for creating the rotating line 
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of 
    # the duration of animation 
    counttime = total_seconds     
      
    # pointer for travelling the loading string 
    i = 0                     
  
    while (counttime != 100): 
          
        # used to change the animation speed 
        # smaller the value, faster will be the animation 
        time.sleep(0.075)  
                              
        # converting the string to list 
        # as string is immutable 
        load_str_list = list(load_str)  
          
        # x->obtaining the ASCII code 
        x = ord(load_str_list[i]) 
          
        # y->for storing altered ASCII code 
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered 
        # switch uppercase to lowercase and vice-versa  
        if x != 32 and x != 46:              
            if x>90: 
                y = x-32
            else: 
                y = x + 32
            load_str_list[i]= chr(y) 
          
        # for storing the resultant string 
        res =''              
        for j in range(ls_len): 
            res = res + load_str_list[j] 
              
        # displaying the resultant string 
        sys.stdout.write("\r"+res + animation[anicount]) 
        sys.stdout.flush() 
  
        # Assigning loading string 
        # to the resultant string 
        load_str = res 
  
          
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len 
        counttime = counttime + 1
