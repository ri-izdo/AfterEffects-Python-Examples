import pyperclip
import pandas as pd
import math
from io import StringIO
import sys

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
    print(keyframeData)
    df = pd.read_csv(keyframeData, sep = '\t')
    print(df)
    
    # global keyframeCount
    # keyframeCount = len(df.index) - 1 # Subtract "End of KeyframeData"
    # # print(f"keyframeCount: {keyframeCount}")
    # # Start at 15 
    # # print(keyframeCount)
    # counter = 15 # Subtract -15 to start tracking positional data.    
    # parameter_list = ["Frame", "X", "Y", "Z"]
    # keyframe_data_list = []

    # # Create list
    # for item in range(keyframeCount):
    #     keyframe_data_list.append(df.iloc[item,0])
    
    # count = -1
    # for key in range(counter, keyframeCount):
    #     if count >= 3:
    #         count = 0
    #         # print(f"key: {key} param: {parameter_list[count]} {keyframe_data_list[key]}")
    #         param = parameter_list[count]
    #         print("Up")
    #         # print(param)
    #         # if param == "Frame":
    #         #     print("Frame")
    #     else:
    #         count += 1
    #         # print(f"key: {key} param: {parameter_list[count]} {keyframe_data_list[key]}")
    #         param = parameter_list[count]
    #         print("Down")
    #         # print(param)
    #         # if param == "X":
    #         #     print("X")
    #         # if param == "Y":
    #         #     print("Y")
    #         # if param == "Z":
    #         #     print("Z")


        
            


        # print(df.iloc[item, 0])
        # # Frame
        # print(f"Frame: {df.iloc[item, 0]}")
        # # X Position
        # print(f"X Position: {df.iloc[item, 0]}")
        # # Y Position
        # print(f"Y Position: {df.iloc[item, 0]}")
        # # Z Position (skip)

    # Extract time and position values
    # for keyframeIndex in range(keyframeCount):
        # keyTime = df.iloc[keyframeIndex, 0]
        # print(f"keyTime {keyframeIndex}: {keyTime}")
        # keyPosition = [df.iloc[keyframeIndex, 0], df.iloc[keyframeIndex, 2]]
        # print(keyPosition)
        # print(keyPosition)
        # keyPosition_x = #[df.iloc[keyframeIndex, 2], df.iloc[keyframeIndex, 4]]
        # print(keyPosition_x)
    #     # Create parsed keyframe object and add to array
    #     parsedKeyframe = ParsedKeyFrameClass()
    #     parsedKeyframe.time = keyTime
    #     parsedKeyframe.position = keyPosition
    #     parsedKeyframes.append(parsedKeyframe)

    # return parsedKeyframes

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
	keyEntry += '\t\t\t<time>' + str(keyTime * frameTime) + ' 153600 1 0</time>\n'
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
            # print(f"time: {parsedKeyframe.time}")
            # print(f"Position: {parsedKeyframe.position[loopCount]}")
            outputString = generateKeyEntryString(parsedKeyframe.position[0], parsedKeyframe.time)

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

def main():

	# print(bcolors.WARNING + bcolors.BOLD + "Attempting to parse After Effects Keyframe data... " + bcolors.ENDC)

	# Parse after effects data from clipboard
	parsedKeyframes = parseAfterEffectsData(pyperclip.paste())

	# # Format after effects data for Motion
	# outputString = generateMotionFormattedString(parsedKeyframes)


	# # Print string and copy to clipboard
	# #print(bcolors.WARNING + bcolors.BOLD + "Copying formatted string to clipboard... " + bcolors.ENDC)
	# # print(outputString)
	# pyperclip.copy(outputString)

main()


