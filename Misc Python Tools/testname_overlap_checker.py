import os

# path to disco repo
defaultDiscoPath = "D:\\git\\Disco"

# path from disco repo to each TestSuite.cs file
testSuitePath = [
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\AddinTestSuite\\AddinTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\AnalyzeTestSuite\\AnalyzeTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\DailyTestSuite\\DailyTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\DesignTestSuite\\DesignTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\ExploreTestSuite\\ExploreTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\LicenseTestSuite\\LicenseTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\PerformanceTestSuite\\PerformanceTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\JournalTests\\BackcompatTestSuite\\BackcompatTestSuite.cs",
    "\\Testing\\Disco.Integration.Tests\\Automation\\ConfigurationTests.cs",
    "\\Testing\\Disco.Integration.Tests\\Automation\\FluidWorkflowTests.cs",
    "\\Testing\\Disco.Integration.Tests\\Automation\\StructuralWorkflowTests.cs",
    "\\Testing\\Disco.Integration.Tests\\Automation\\ThermalWorkflowTests.cs"
    ]

# prompt user for disco path and check exists
while True:
    discoPath = input("Enter location of your Disco repo (Default: " + defaultDiscoPath + "):\n")
    if discoPath == "":
        discoPath = defaultDiscoPath
    if os.path.exists(discoPath):
        break

# extracting list of test names from TestSuite.cs files
testNames = []
for path in testSuitePath:
    if os.path.exists(discoPath + path):
        with open(discoPath + path, "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                if "public async Task" in line:
                    if line.strip().split("public async Task")[1].split("()")[0].strip() not in testNames:
                        testNames.append(line.strip().split("public async Task")[1].split("()")[0].strip())
                elif "public void" in line:
                    if line.strip().split("public void")[1].split("()")[0].strip() not in testNames:
                        testNames.append(line.strip().split("public void")[1].split("()")[0].strip())

# print list of test names and number of tests
testNames.sort()
for name in testNames:
    print(name)
print("\nTotal: "+str(len(testNames))+"\n")

# grouping together test names that overlap
overlappingNames = []
for name1 in testNames:
    temp = []
    for name2 in testNames:
        if name1 == name2:
            continue
        elif name1 in name2:
            temp.append(name2)
    if len(temp)>0:
        temp.append(name1)
        temp.sort(key=len)
        if temp not in overlappingNames:
            overlappingNames.append(temp)

# print overlapping test name results
for group in overlappingNames:
    temp = group[0] + " | "
    for i in range(1,len(group)-1):
        temp += group[i] + ", "
    temp += group[-1]
    print(temp)
total = 0
for group in overlappingNames:
    total += len(group)
print("\nTotal overlapping test names: "+str(total))

# needed to keep the program window open when running the script by double clicking on the .py file
input('\nPress ENTER to exit')