# Filename:     JournalToScript_Replacer.py
# Author:       Ethan Markowski
# Date:         December 8, 2021
#  
# Description:  # This can be used to replace scjournals in the Disco repository with recorded script conversions. All scripts in the specified directory
#               are matched up with the corresponding journals in the repo and swapped out. Additionally, the RunJournalTest and RunJournalTestStep
#               method calls in the TestSuite.cs files are updated to RunScriptTest and RunScriptTestImpl methods pointing to the new script files.
#               he csproj file is also updated so that the new scripts are included in the DiscoTesting solution.
#
#               From here, you can open the DiscoTesting solution in Visual Studio and run all tests with the JournalRegressionTest trait to run all of the
#               converted scripts to check for playback errors.

import os
import shutil
import sys

defaultDiscoRepoPath = r"D:\git\Disco"
csprojPath = ""

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
scriptPath = getPath("path to scripts")

# Locate Disco.Integration.Tests.csproj
for (root, dirs, filenames) in os.walk(discoRepoPath):
        for filename in filenames:
            if filename == "Disco.Integration.Tests.csproj":
                csprojPath = os.path.join(root, filename)
                break

# If csproj file was not found
if csprojPath == "":
    print("Disco.Integration.Tests.csproj not found")
    input("Press enter to exit")
    sys.exit

# Replace scjournals with recorded script conversions and make corresponding modifications in TestSuite.cs files
for scriptName in os.listdir(scriptPath):
    if scriptName.endswith(".py"):
        journalName = scriptName.replace(".py", ".scjournal")
    elif scriptName.endswith(".scscript"):
        journalName = scriptName.replace(".scscript", ".scjournal")

    # Locate and open TestSuite.cs files
    for (root, dirs, filenames) in os.walk(discoRepoPath):
            for filename in filenames:
                if filename.endswith("TestSuite.cs"):
                    with open(os.path.join(root, filename), 'r') as fileObj:
                        lines = fileObj.read().splitlines()
                        
                    # Replace .scjournal references and method calls
                    newLines = []
                    isJournalReplaced = False
                    for line in lines:
                        if "RunJournalTest(" in line and journalName in line:
                            line = line.replace("RunJournalTest(", "RunScriptTest(").replace(journalName, scriptName)
                            isJournalReplaced = True
                        elif "RunJournalTestStep(" in line and journalName in line:
                            line = line.replace("RunJournalTestStep(", "RunScriptTestImpl(").replace(journalName, scriptName)
                            isJournalReplaced = True
                        elif " : BaseJournalTest" in line:
                            line = line.replace(" : BaseJournalTest", " : BaseScriptTest")
                        newLines.append(line)

                    # Add "using Ansys.Disco.TestFramework.Script;" directive if not already included in the file
                    includeDirective = "using Ansys.Disco.TestFramework.Script;"
                    if includeDirective not in newLines:
                        newLines.insert(2, includeDirective)

                    # If any references were replaced
                    if newLines != lines:

                        # Save changes to TestSuite.cs file
                        with open(os.path.join(root, filename), 'w') as fileObj:
                            fileObj.write('\n'.join(newLines))

                    # Copy script into test folder for TestSuite and delete journal
                    if isJournalReplaced == True:
                        try:
                            shutil.copy2(os.path.join(scriptPath, scriptName), os.path.join(root, "Tests", scriptName))

                            # Update references in the .csproj file
                            with open(csprojPath, 'r') as fileObj:
                                lines = fileObj.read().splitlines()
                            newLines = [line.replace(journalName, scriptName) for line in lines]   
                            with open(csprojPath, 'w') as fileObj:
                                fileObj.write('\n'.join(newLines)) 

                            try:
                                os.remove(os.path.join(root, "Tests", journalName))
                            except:
                                print("Error deleting file: {}".format(journalName))
                        except:
                            print("error copying file: {}".format(scriptName))   
