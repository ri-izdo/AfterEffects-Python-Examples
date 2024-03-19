import os
import sys
import json
import csv
import subprocess
import pyperclip
import pandas as pd
import math
from io import StringIO
import sys

SCRIPTS = os.path.abspath("")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import AE_configuration as config
import AE_keyframe_converter as keyframe_converter

try:
    TASK_LIST_CSV = sys.argv[1]

except ValueError:
    print("Error: AE_Tasklist.py constants required.")

# Multiplier for AE Seconds to whatever Motion uses
frameTime = 5120

# Global variables
keyframeCount = 0

# Class for storing time and position keyframe data
class ParsedKeyFrameClass:
	time = 0
	position = [0, 0, 0]

# Parse after effects clipboard data
def parseAfterEffectsData(data):
	# Handle incorrect data
    headerString = data.split('\n')[0]
    # print(headerString)
	
    parsedKeyframes = []

    # Isolate composition data
    compData = data.split('\n')[2:7]
    compFrameRate = compData[0].split('\t')[2]
    # print(compFrameRate)

    # Isolate keyframe data
    keyframeData = data.split('\n\n')[0]
    # print(keyframeData)
    keyframeData = keyframeData.split('\t')[1:]
    # print(keyframeData)
    keyframeData = "\n".join(keyframeData)
    # print(keyframeData)

    # # Create dataframe from keyframe data
    keyframeData = StringIO(keyframeData)
    # print(keyframeData)
    df = pd.read_csv(keyframeData, sep = '\t')
    # print(df)

    global keyframeCount
    keyframeCount = len(df.index) - 1# Subtract "End of KeyframeData"
    # print(f"keyframeCount: {keyframeCount}")
    # Start at 15 
    # print(keyframeCount)
    counter = 15 # Subtract -15 to start tracking positional data.    
    parameter_list = ["Frame", "X", "Y", "Z"]
    keyframe_data_list = []

    # Create list
    for item in range(keyframeCount):
        keyframe_data_list.append(df.iloc[item,0])
    
    keydata_dict = {}
    # Append as Frame, X pos, Y pos, Z pos
    count = 0
    for key in range(counter, keyframeCount):
        param = parameter_list[count]
        if param == "Frame":
            frame = keyframe_data_list[key]
            x = key + 1
            x_pos = keyframe_data_list[x]
            # Create parsed key frames.
            parsedKeyframe = ParsedKeyFrameClass()
            parsedKeyframe.time = int(frame)
            parsedKeyframe.position = x_pos
            parsedKeyframes.append(parsedKeyframe)

            # y = parameter_list[2]
            # z = parameter_list[3]
        count += 1
        if count > 3:
            count = 0
        else:
            pass 


        # if count < 4:
        #     param = parameter_list[count]
        #     if param == "Frame":
        #         frame_number = keyframe_data_list[key]
        #         print(frame_number)
        #     count += 1
        # else:
        #     count = 0
        #     pass
    #     if count > 3:
    #         print("Do no count")
    #         count = 0
    #     else:
    #         print(f"Count:{count}")
    #         count += 1

    return parsedKeyframes

# Write header for Motion data
def generateHeaderString(name = "X", id = "1"):
	header = ''
	header += '<parameter name="' + str(name) + '" id="' + str(id) + '" flags="8606711824">\n'
	header += '\t<curve type="1" default="0" value="0">\n'
	header += '\t\t<numberOfKeypoints>' + str(keyframeCount) + '</numberOfKeypoints>\n'

	return header

# First entry for Motion data has no input tangents
def generateFirstKeyEntryString(keyValue, outputTangentTime = 0.011111111111111112, outputTangentValue = 0.33333333333333331):
	firstKeyEntry = ''
	firstKeyEntry += '\t\t<keypoint flags="0">\n'
	firstKeyEntry += '\t\t\t<time>0 1 1 0</time>\n'
	firstKeyEntry += '\t\t\t<value>' + str(keyValue) + '</value>\n'
	firstKeyEntry += '\t\t\t<outputTangentTime>' + str(outputTangentTime) + '</outputTangentTime>\n'
	firstKeyEntry += '\t\t\t<outputTangentValue>' + str(outputTangentValue) + '</outputTangentValue>\n'
	firstKeyEntry += '\t\t</keypoint>\n'

	return firstKeyEntry

# Write key entry for Motion data
def generateKeyEntryString(keyValue, keyTime, inputTangentTime = 0.011111111111111112, inputTangentValue = -0.33333333333333331, outputTangentTime = 0.011111111111111112, outputTangentValue = 0.33333333333333331):

	keyEntry = ''
	keyEntry += '\t\t<keypoint flags="0">\n'
	keyEntry += '\t\t\t<time>' + str(keyTime * 5120) + ' 153600 1 0</time>\n'
	keyEntry += '\t\t\t<value>' + str(keyValue) + '</value>\n'
	keyEntry += '\t\t\t<inputTangentTime>' + str(inputTangentTime) + '</inputTangentTime>\n'
	keyEntry += '\t\t\t<inputTangentValue>' + str(inputTangentValue) + '</inputTangentValue>\n'
	keyEntry += '\t\t\t<outputTangentTime>' + str(outputTangentTime) + '</outputTangentTime>\n'
	keyEntry += '\t\t\t<outputTangentValue>' + str(outputTangentValue) + '</outputTangentValue>\n'
	keyEntry += '\t\t</keypoint>\n'

	return keyEntry

# Generate motion formatted string

def generateMotionFormattedString(parsedKeyframes):

    # print(f"parsedKeyframes{parsedKeyframes}")

    # Write header
    outputString = ''

    # X Axis
    outputString += generateHeaderString(name = 'X', id = '1')
    # print(f"outputString: {outputString}")

    for parsedKeyframe in parsedKeyframes:
        if (parsedKeyframe.time == 0):
            # Write first key
            # print(f"time: {parsedKeyframe.time}")
            outputString = generateFirstKeyEntryString(parsedKeyframe.position[0])
        else:
            # print(f"time: {parsedKeyframe.time} pos: {parsedKeyframe.position}")
            # print(f"Position: {parsedKeyframe.position[loopCount]}")
            outputString = generateKeyEntryString(parsedKeyframe.position, parsedKeyframe.time)

    outputString += '\t</curve>\n</parameter>\n'
    # print(f"{outputString}")

	# # Y Axis
    # outputString += generateHeaderString(name = 'Y', id = '2')

    # for parsedKeyframe in parsedKeyframes:
    #     if (parsedKeyframe.time == 0):
    #         # Write first key
    #         # print(f"time: {parsedKeyframe.time}")
    #         outputString = generateFirstKeyEntryString(parsedKeyframe.position[1])
    #     else:
    #         # print(f"time: {parsedKeyframe.time}")
    #         # print(f"Position: {parsedKeyframe.position[loopCount]}")
    #         outputString = generateKeyEntryString(parsedKeyframe.position[1], parsedKeyframe.time)

    # outputString += '\t</curve>\n</parameter>\n'
    # print(f"{outputString}")

	# # # Z Axis
    # outputString += generateHeaderString(name = 'Z', id = '3')

    # for parsedKeyframe in parsedKeyframes:
    #     if (parsedKeyframe.time == 0):
    #         # Write first key
    #         # print(f"time: {parsedKeyframe.time}")
    #         outputString = generateFirstKeyEntryString(0)
    #     else:
    #         # print(f"time: {parsedKeyframe.time}")
    #         # print(f"Position: {parsedKeyframe.position[loopCount]}")
    #         outputString = generateKeyEntryString(0, parsedKeyframe.time)

    # outputString += '\t</curve>\n</parameter>\n'
    # # print(outputString)

    return outputString

def convert_keyframes():
    '''Reads CSV File for task parameters.
    '''
    column = ["afterEffects_file_list","motion_file_list","motion_layer_list"]
    afterEffects_file_list = []
    motion_file_list = []
    motion_layer_list = []
    with open(TASK_LIST_CSV) as csvfile:
        csvread = csv.reader(csvfile)
        for i, row in enumerate(csvread):
            if i == 0: continue

            # Open After Effects File. Have user copy keyframe data.
            try:
                config.close_app("After Effects")
            except:
                pass
            after_effects_path = row[0]
            cmd = [
                "open",
                after_effects_path
            ]
            subprocess.call(cmd)
            ppid = os.getppid()

            ae_interact = input("Copy the After Effects Position key frames and press Return to continue...")

            cmd = [
                "osascript",
                "-e",
                'quit app "After Effects"' 
            ]
            subprocess.call(cmd)

            parsedKeyframes = parseAfterEffectsData(pyperclip.paste())

            outputString = generateMotionFormattedString(parsedKeyframes)

            pyperclip.copy(outputString)
        
            # Transfer to Motion File.
            



            # afterEffects_file_list.append(row[0])
            # motion_file_list.append(row[1])
            # motion_layer_list.append(row[2])

#     task_row = []
#     for file_number in range(len(afterEffects_file_list)):
#         params = [
#             str(afterEffects_file_list[file_number]),
#             str(motion_file_list[file_number]),
#             str(motion_layer_list[file_number])
#             ]
#         task_row.append(params)

#     # Remove csvfile
#     rm_csv_cmd = [
#         "rm",
#         TASK_LIST_CSV
#     ]
#     # subprocess.call(rm_csv_cmd)
#     return task_row

# # Open After Effects file.
# def open_files(task_row):
#     for i in range(0, len(task_row)):



if __name__ == '__main__':
    try:
        task_row = convert_keyframes()
        
        # open_files(task_row)

    except ValueError:
        print("Error: AE_tasklist.py")
