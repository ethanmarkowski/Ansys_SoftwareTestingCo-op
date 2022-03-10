import os

machinesPath = input("Enter file location of Machines.txt (Default: D:\\git\\Disco\\Tools\\PerformanceTool\\Machines.txt):\n")
if machinesPath == '' or machinesPath == ' ':
    #Default path for Machines.txt
    machinesPath = "D:\\git\\Disco\\Tools\\PerformanceTool\\Machines.txt"

machines = open(machinesPath, "r").readlines()
machinesText = machines[1:]

testName = input("Enter the name of the test with the scenario (don't include .scjournal):\n")
oldName = input("Enter the old name of the scenario:\n")
newName = input("Enter the new name of the scenario:\n")

#get test name without prefix
if(len(testName.split('Perf_')) > 1):
    testNameNoPerf = testName.split('Perf_')[1]
else:
    testNameNoPerf = testName

#declaring variables to be used
perfPath = ""
baseLinePath = ""
logPaths = []
csvPaths = []

#go through each machine
for tester in machinesText:
    #format file path
    pathList = tester.split("\n")[0].split("\\")
    path = "\\\\" + pathList[2] + "\\" + pathList[3]

    #get path of log, and _performance files
    if os.path.exists(path):
        for log in os.listdir(path):
            if log == testName + ".log":
                logPaths.append(path + "\\" + log)
            if log == testName + "_performance.csv":
                csvPaths.append(path + "\\" + log)

#change tag in log files
for test in logPaths:
    with open(test, "r+") as fd:
        filedata = fd.read()
        filedata = filedata.replace(", " + oldName + ",", ", " + newName + ",")
    with open(test, "w") as fd:
        fd.write(filedata)

#change tag in _performance.csv files
for test in csvPaths:
    with open(test, "r+")  as fd:
        filedata = fd.read()
        filedata = filedata.replace("\n" + oldName + ",", "\n" + newName + ",")
    with open(test, "w") as fd:
        fd.write(filedata)
