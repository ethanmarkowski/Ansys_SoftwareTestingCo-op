import os
import argparse
from datetime import datetime
import sys

#Change a string representation of a duration into a float
def time_to_sec(time):
    if time == '':
        return 0
    else:
        holder = time.strip().split(":")
        if len(holder) == 1:
            return float(holder[0])
        hour = int(holder[0])
        minute = int(holder[1])
        sec = float(holder[2])
        return hour * 3600 + minute * 60 + sec

#combine files to into main file
def combine(path, testNames):
    combined = open(path + "\\Performance.csv", 'w')
    combined.write("Scenario,Test Name,Time (s),Date,Machine,Version\n")
    for test in testNames.values():
        base = open(defaultPath + "\\" + test + "_performance.csv", 'r')
        baseData = base.readlines()[1:]
        combined.writelines(baseData)
        base.close()
    combined.close()

#declaring variables to be used
scenario = {}
testName = {}
time = {}
date = {}
data = {}
test = {}
dateAll = []
baselineData = {}
dateBaseline = {}

#process command line arguments
parser = argparse.ArgumentParser(description = "Collect Performance Data")
parser.add_argument("--logs", default = '', help = "Location of performance logs and where files will be saved")
parser.add_argument("--machines", default = '', help = "Location of Machines.txt file")
parser.add_argument("--install", default = '', help = "Location of Disco Install directory")
args = parser.parse_args()

#checking if default file path is desired
if len(sys.argv) == 1:
    #default path to save files
    defaultPath = "C:\\ANSYSDev\\PerformanceLogging"
    print("Performance data will be saved to: " + defaultPath)
    doDefault = input("Would you like to change this path? Input 'y' for yes, otherwise press 'ENTER':\n")
    if doDefault.lower() == 'y' or doDefault.lower() == "yes":
        #set new path for saving files
        defaultPath = input("Enter desired file path: ")
        print("Saving to: " + defaultPath)
else:
    defaultPath = args.logs

#get machine names and filepaths
if len(sys.argv) == 1:
    machinesPath = input("Enter file location of Machines.txt (Default: D:\\git\\Disco\\Tools\\PerformanceTool\\Machines.txt):\n")
    if machinesPath == '' or machinesPath == ' ':
        #Default path for Machines.txt
        machinesPath = "D:\\git\\Disco\\Tools\\PerformanceTool\\Machines.txt"
else:
    machinesPath = args.machines
machines = open(machinesPath, "r").readlines()
machines = machines[1:]

#get version number
if len(sys.argv) == 1:
    versions = []
    version = ''
    installPath = input("Enter location of your local Disco install (Default: C:\\ANSYSDev\\Disco_Install):\n")
    if installPath == '' or installPath == ' ':
        installPath = "C:\\ANSYSDev\\Disco_Install"
    for directory in os.listdir(installPath):
        if directory.startswith('v'):
            versions.append(directory.split('v')[1])
    for v in versions:
        if v > version:
            version = v
else:
    version = args.install

#go through each machine
for tester in machines:
    #format file path
    pathList = tester.split("\n")[0].split("\\")
    path = "\\\\" + pathList[2] + "\\" + pathList[3]
    print(path)

    #get the name of the machine running the program
    machine = pathList[2]

    #scan through every file in directory
    if os.path.exists(path):
        for tests in os.listdir(path):
            #check if file is valid
            if tests.endswith(".log"):
                #get the name of the file without prefix or affix
                testName[tests] = tests.split(".")[0]

                #opening input and output files
                fileData = open(path + "\\" + tests, "r")

                #getting all lines from log files and sorting to get newest first
                logLines = fileData.readlines()
                logLines.reverse()

                #creating variable to store preexisting file lines
                lines = []
                
                #check if output files already exist
                if os.path.exists(defaultPath + "\\" + testName[tests] + "_performance.csv"):
                    #loads data from file to use for checking
                    output = open(defaultPath + "\\" + testName[tests] + "_performance.csv", "r")
                    lines = output.readlines()
                    output.close()

                    #open file to append data
                    output = open(defaultPath + "\\" + testName[tests] + "_performance.csv", "a")
                else:
                    #create new output file
                    output = open(defaultPath + "\\" + testName[tests] + "_performance.csv", "w")

                    #creating header
                    output.write("Scenario,Test Name,Time (s),Date,Machine,Version\n")

                #get test name without prefix
                if(len(testName[tests].split('Perf_')) > 1):
                    testNameNoPerf = testName[tests].split('Perf_')[1]
                else:
                    testNameNoPerf = testName[tests]
                if testNameNoPerf not in baselineData:
                    baselineData[testNameNoPerf] = {}
                    dateBaseline[testNameNoPerf] = {}

                #scan and format data and add to output file
                for line in logLines:
                    data[line] = line
                    splitData = data[line].split(", ", 3)
                    date[line] = splitData[0].split(" ")[0]
                    scenario[line] = splitData[1]
                    time[line] = time_to_sec(splitData[3].split(", ")[0])
                    baseline = splitData[2].split(':')
                    baseTime = int(baseline[0]) * 3600 + int(baseline[1]) * 60 + float(baseline[2])
                    if scenario[line] not in baselineData[testNameNoPerf].keys():
                        baselineData[testNameNoPerf][scenario[line]] = baseTime
                        dateBaseline[testNameNoPerf][scenario[line]] = date[line]
                    elif baselineData[testNameNoPerf][scenario[line]] != baseTime:
                        basedate = datetime.strptime(dateBaseline[testNameNoPerf][scenario[line]], "%m/%d/%Y")
                        newdate = datetime.strptime(date[line], "%m/%d/%Y")
                        if basedate < newdate:
                            baselineData[testNameNoPerf][scenario[line]] = baseTime
                            dateBaseline[testNameNoPerf][scenario[line]] = date[line]

                    #line of data to be printed onto file
                    outputLine = str(scenario[line]) + "," + str(testName[tests]) + "," + str(time[line]) + "," + str(date[line]) + "," + machine + "," + str(version) + "\n"

                    #if data already exists, it is skipped
                    if outputLine not in lines:
                        #print data into csv format
                        output.write(outputLine)

                #close all files
                fileData.close()
                output.close()

#combine files
combine(defaultPath, testName)

#removing scenario from Perf_MultiSim that has been renamed
if "MultiSim" in baselineData.keys():
    if "Solve Structural Analyze" in baselineData["MultiSim"].keys():
        del baselineData["MultiSim"]["Solve Structural Analyze"]

#create spreadsheet with Baseline Data
csv = open(defaultPath + "\\Baseline Data.csv", 'w')
csv.write("Scenario,Test Name,Time (s)\n")
for test in baselineData.keys():
    for scenario in baselineData[test].keys():
        csv.write(scenario + ',' + test + ',' + str(baselineData[test][scenario]) + '\n')
csv.close()