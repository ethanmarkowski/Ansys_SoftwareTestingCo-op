# Filename:     JournalToScript_Recorder.py
# Author:       Ethan Markowski
# Date:         December 8, 2021
#  
# Description:  This script can be used to modify each scjournal in your Disco repository so that at the start of the journal, 
#               the script editor will open and begin a script recording. The recorded script will then be saved to a specified
#               directory path at the end of the journal.
#
#               Use this python script to modify your local journals and then run all journal tests in Visual Studio to generate
#               a script conversion of each scjournal in the Disco repo.

import os
import sys

defaultDiscoRepoPath = r"D:\git\Disco"

# journal lines for script editor record and save
startScriptRecordSmartVariables = [
    "S=1,UI_CMD=Disco.ShowScript",
    "S=1,ScriptApiChangedAction,V22 Beta",
    "S=1,UI_CMD=ScriptEditorSelectBySmartVariable_0",
    "S=1,ScriptSetRecordAction,True",
    "S=1,UI_CMD=ScriptEditorRecord_0",
    "S=1,ScriptSetRecordAction,True"
]

startScriptRecordIndexSelection = [
    "S=1,UI_CMD=Disco.ShowScript",
    "S=1,ScriptApiChangedAction,V22 Beta",
    "S=1,UI_CMD=ScriptEditorSelectByIndex_0",
    "S=1,ScriptSetRecordAction,True",
    "S=1,UI_CMD=ScriptEditorRecord_0",
    "S=1,ScriptSetRecordAction,True"
]

saveScript = "S=1,ScriptSaveAction,{}"

# prompt user to input or confirm a path
def getPath(pathName, defaultPath=""):
    pathInput = input("\n{}: {}\npress Enter to confirm or input path:\n".format(pathName, defaultPath))

    path = defaultPath if pathInput == "" else pathInput

    if not os.path.exists(path):
        print("path: {} does not exist".format(path))
        input("\nPress enter to exit")
        sys.exit()
    
    return path

discoRepoPath = getPath("disco repo path", defaultDiscoRepoPath)
scriptSavePath = getPath("path for the journals to save the scripts they record to")

scriptType = int(input("\ninput 1 for Smart Variable scripts or 2 for Index Selection scripts\n"))
if not (scriptType == 1 or scriptType == 2):
    print("invalid entry")
    sys.exit()

# locate and load .scjournal files
for (root, dirs, filenames) in os.walk(discoRepoPath):
        for filename in filenames:
            if filename.endswith(".scjournal"):
                with open(os.path.join(root, filename), 'r') as fileObj:
                    try:
                        lines = fileObj.read().splitlines()
                    except:
                        print("error opening file - {}".format(filename))

                # find "S=1," in journal file
                index = -1
                for i, line in enumerate(lines):
                    if "S=1," in line:
                        index = i
                        break
                if index == -1:
                    print("\"S=1,\" not found in: {} - skipping file".format(filename))
                    continue

                # create journal to record script with Smart Variables
                if scriptType == 1:
                    try:
                        with open(os.path.join(root, filename), 'w') as fileObj:
                            newLines = lines[0:index] + startScriptRecordSmartVariables + lines[index:] + [saveScript.format(os.path.join(scriptSavePath, filename.replace(".scjournal", ".scscript")))]
                            fileObj.write("\n".join(newLines))
                    except:
                        print("error saving file - {}".format(filename))

                # create journal to record script with Index Selection
                elif scriptType == 2:
                    try:
                        with open(root+'\\'+filename, 'w') as fileObj:
                            newLines = lines[0:index] + startScriptRecordIndexSelection + lines[index:] + [saveScript.format(os.path.join(scriptSavePath, filename.replace(".scjournal", ".py")))]
                            fileObj.write("\n".join(newLines))
                    except:
                        print("error saving file - {}".format(filename))
