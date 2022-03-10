from datetime import datetime, timedelta
import argparse
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.backends.backend_pdf
from matplotlib import ticker
import os
import sys
import subprocess
import time

defaultLogsPath = "C:\\ANSYSDev\\PerformanceLogging"
defaultBugPath = "D:\\git\\Parts\\Discovery\\Unified\\Tools\\GetBugs"
reportRange = 60
machineCheck = ["CHQ2DISCOTEST04"]

#returns datetime version of string date
def datetimeParse(date):
    return datetime.strptime(date, "%m/%d/%Y")

# returns dictionaries of baselines and average times for all scenarios
# baselines are the official baselines established in the test
# historical baselines are calculated by adding the standard deviation and 110% of the average data for each scenario
# average times and historical baselines are calculated only using data from the last 60 days
def getBaselines(reportRange, path, machines):
    import math

    dateCutoff = datetime.today() - timedelta(days=reportRange)

    f = open(path + "\\Performance.csv", 'r')
    filedata = f.read().splitlines()[1:]
    f.close()
    f = open(path + "\\Baseline Data.csv", 'r')
    baselineData = f.read().splitlines()[1:]
    f.close()

    scenarios = []
    averages = {}
    counts = {}
    differences = {}
    standardDeviations = {}
    historicalBaselines = {}
    baselines = {}

    filedata.sort(key = lambda date: datetimeParse(date.split(',')[3]), reverse = True)

    # retrieve test baselines
    for line in baselineData:
        baselines[line.split(',')[0]] = float(line.split(',')[2])

    # calculate historical baselines
    for scenario in baselines.keys():
        sum = 0
        count = 0
        diffSum = 0
        counts[scenario] = 0

        # calculate 60 day average time
        for line in filedata:
            splitLine = line.split(',')

            # restrict data to specified machines and dateCutOff
            if (splitLine[0] == scenario and (splitLine[4] in machines)):
                if (datetimeParse(splitLine[3]) < dateCutoff):
                    break
                time = float(splitLine[2])
                sum += time
                count += 1

        # calculate average time
        if count > 0:
            averages[scenario] = sum / count
            counts[scenario] = count

        # calculate 60 day standard deviation and historical baseline
        count = 0
        for line in filedata:
            splitLine = line.split(',')
            time = float(splitLine[2])
            if (splitLine[0] == scenario and (splitLine[4] in machines)):
                diffSum += (time - averages[scenario]) * (time - averages[scenario])
                count += 1
            if count == counts[scenario]:
                break
        if counts[scenario] > 0:
            differences[scenario] = diffSum
            standardDeviations[scenario] = math.sqrt(differences[scenario] / counts[scenario])
            historicalBaselines[scenario] = averages[scenario]*1.1 + (standardDeviations[scenario])

    return baselines, historicalBaselines, averages

#process command line arguments
parser = argparse.ArgumentParser(description = "Collect Performance Data")
parser.add_argument("--logs", default = '', help = "Location of performance logs and where files will be saved")
parser.add_argument("--save", default = '', help = "Where to save PerfReport.pdf")
parser.add_argument("--bugs", default = '', help = "Location of GetBugs.exe")
parser.add_argument("--key", default = '', help = "PAT Key for TFS")
parser.add_argument("--tests", default = '', help = "List of tests to be included")
args = parser.parse_args()

#checking if default file path is desired
if len(sys.argv) == 1:
    logsPath = input("Enter directory that holds performance logs (Default: C:\\ANSYSDev\\PerformanceLogging):\n")
    savePath = "PerfReport.pdf"
    if logsPath == '' or logsPath == ' ':

        #Default Performance Logging directory
        logsPath = defaultLogsPath
    bugPath = input("Enter file location of GetBugs.exe (Default: D:\\git\\Parts\\Discovery\\Unified\\Tools\\GetBugs):\n")
    if bugPath == '' or bugPath == ' ':

        #Default path for GetBugs.exe
        bugPath = defaultBugPath

    #setting value for key
    if 'TFS_PAT' in os.environ:
        key = os.environ['TFS_PAT']
    else:
        key = input("Input PAT:\n")

    # Get bugs reported in tests
    tests = ["CertWorkflow_SaveThermalMix_ResumeThermalMix",
            "Material_Local_Save",
            "Params_TestCase_SaveResume_UndoRedo",
            "Perf_Base",
            "Perf_BearingLoadBoltPreload",
            "Perf_CHT_ExternalFlow",
            "Perf_CHT_PullAndMesh",
            "Perf_ConvertJoints",
            "Perf_DesignTools",
            "Perf_Detach_All",
            "Perf_FileOpen_Car",
            "Perf_Fluids_Basic",
            "Perf_Hide_Show",
            "Perf_Import_Contacts_Materials",
            "Perf_Import_Duplicate_Delete",
            "Perf_Mesh",
            "Perf_MoveUndo",
            "Perf_MultiSim",
            "Perf_NonLinearContact_Modal",
            "Perf_OpenFiles",
            "Perf_Open_Parameters",
            "Perf_Pull_Upto",
            "Perf_StructuralAnalyze",
            "QuickStart_external_smart_suppress_Explore",
            "SampleModel_Topo",
            "ShareTopo_Slidercrank_issue",
            "ShareTopo_Unshare",
            "Structural_LocalSimOptions_Nonlinear2Linear",
            "TurbulentHTBackwardStep_4_4",
            "Volume_extract_with_internal_bodies"]
else:
    logsPath = args.logs
    savePath = args.save + "\\PerfReport.pdf"
    bugPath = args.bugs
    key = args.key
    tests = args.tests.split(',')

testBugs = {}
for test in tests:
    subprocess.Popen(bugPath + "\\GetBugs.exe " + test + " " + bugPath + " " + key).wait(timeout=None)
    with open(bugPath + "\\Bugs.txt", 'r') as file:
        testBugs[test] = file.readlines()

#declaring variables to be used
perfPath = ""
baseLinePath = ""
results = {}
latest = {}
numValues = {}
lastDate = {}

#get path of Perfomance.csv and BaseLine Data.csv
if os.path.exists(logsPath):
    for log in os.listdir(logsPath):
        if log == "Performance.csv":
            perfPath = logsPath + "\\" + log
        if log == "Baseline Data.csv":
            baseLinePath = logsPath + "\\" + log

#get results from Performance.csv                    
with open(perfPath, "r") as perf:
    perf.readline()
    for line in perf:
        lineData = line.strip().split(",")
        scenario = lineData[0]
        testName = lineData[1]
        time = float(lineData[2].strip())
        date = lineData[3]
        machine = lineData[4]
        version = lineData[5]

        # add testName to results
        if testName not in results:
            results[testName] = {}
            numValues[testName] = {}

        # add scenario to results
        if scenario not in results[testName]:
            results[testName][scenario] = {}
            latest[scenario] = 0
            lastDate[scenario] = datetime.min
            numValues[testName][scenario] = {}
            
        # restrict to specific machines
        if machine in machineCheck:

            # update latest time
            # the latest time is the highest time for the most recent date that has data for the scenario
            if datetimeParse(date) > lastDate[scenario] or (datetimeParse(date) == lastDate[scenario] and time > latest[scenario]):
                latest[scenario] = time
                lastDate[scenario] = datetimeParse(date)

            # add times to results
            if date not in results[testName][scenario]:
                results[testName][scenario][date] = time
                numValues[testName][scenario][date] = 1

            # if there is already a result for this date, average that day's times
            else:
                num = numValues[testName][scenario][date]
                numValues[testName][scenario][date] += 1
                results[testName][scenario][date] = (results[testName][scenario][date] * num + time)/(num + 1)

#remove old results
for testName in results:
    for scenario in results[testName]:
        for date in list(results[testName][scenario]):
            if datetimeParse(date) < datetime.today() - timedelta(days=reportRange):
                del results[testName][scenario][date]

# get baselines          
baselines, historicalBaselines, averages = getBaselines(reportRange, logsPath, machineCheck)

# check if scenario has results from within the last 2 months and if the latest result is higher than both the historical baseline and 105% of the test baseline
for testName in results:
    fails = {}
    for scenario in results[testName]:
        if scenario not in fails:
            fails[scenario] = False
        if scenario in historicalBaselines:
            baseline = baselines[scenario]
            historicalBaseline = historicalBaselines[scenario]

        # use default baseline times of 600 seconds if baselines were not found for scenario
        else:
            baseline = 600
            historicalBaseline = 600

        # check if latest time is higher than both historical baseline and 105% of test baseline
        if lastDate[scenario] > datetime.today() - timedelta(reportRange) and latest[scenario] >= baseline * 1.05 and latest[scenario] > historicalBaseline:
            fails[scenario] = True

    # filter data to only include scenarios that have at least 3 data points, with the most recent run failing the baseline tests
    for scenario in fails:
        if not (fails[scenario]) or (len(results[testName][scenario]) < 3):
            del results[testName][scenario]

# create pdf with graphs
pdf = matplotlib.backends.backend_pdf.PdfPages(savePath)

# formatting for first page of report
rows = 3
columns = 2
fig = plt.figure(figsize=(11, 8.5), constrained_layout=False)
gs = fig.add_gridspec(nrows=rows+2, ncols=columns+2, height_ratios=[3.5, 10, 10, 10, 0.5], width_ratios=[1, 20, 20, 1],
    left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.10, hspace=0.4)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
title = fig.add_subplot(gs[0, :])
title.get_xaxis().set_visible(False)
title.get_yaxis().set_visible(False)
title.set_facecolor('#012456')
title.text(0.008, 0.90, "Performance Report", horizontalalignment="left", verticalalignment="top", color="white", font="Arial", fontsize=20, wrap=True)
title.text(0.01, 0.475, "Machine: " + ",".join(machineCheck) + "\nDate: " + str(datetime.today().strftime("%m/%d/%Y")),
    horizontalalignment="left", verticalalignment="top", color="white", font="Arial", fontsize=10, wrap=True)
footer = fig.add_subplot(gs[-1, :])
footer.get_xaxis().set_visible(False)
footer.get_yaxis().set_visible(False)
footer.set_facecolor('#012456')

# creating subplots for first page of report
plotNum = 0
axes = []
for row in range(1, rows+1):
    axes.append([fig.add_subplot(gs[row, 1]), fig.add_subplot(gs[row, 2])])

# hide axes in subplots that will be used for text entry
for index in range(0, rows):
    axes[index][1].axis("off")

for testName in results:
    for scenario in results[testName]:
        x1 = []
        y1 = []
        latestRun = latest[scenario]
        historicalBaselineScenario = historicalBaselines[scenario]
        baselineScenario = baselines[scenario]

        # format performance data for plot
        for date in sorted(results[testName][scenario], key=datetimeParse):
            dateData = date.split("/")
            x1.append(dateData[0] + "/" + dateData[1])
            y1.append(results[testName][scenario][date])

        # calculate change from average and change from baselines
        changeFromHistoricalBaseline = (latestRun - historicalBaselineScenario) / historicalBaselineScenario * 100
        changeFromBaseline = (latestRun - baselineScenario) / baselineScenario * 100
        if averages[scenario] != 0:
            averageChange = (latestRun - averages[scenario]) / averages[scenario] * 100
        else:
            averageChange = 0
        
        #create graph
        historicalBaseline_line = axes[plotNum][0].axhline(y=historicalBaselineScenario, linewidth=1.3, color="#8d2424")
        baseline_line = axes[plotNum][0].axhline(y=baselineScenario, linewidth=1.3, color="#005C00")
        axes[plotNum][0].plot(x1, y1, color="#012456", linewidth=1.0, marker="o", markersize=3)
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        axes[plotNum][0].legend([historicalBaseline_line, baseline_line], ["Historical Baseline", "Test Baseline"], 
            loc="upper left", ncol=2, fancybox=False, edgecolor="white", borderaxespad=0.15, framealpha=1, prop=font_manager.FontProperties(family="Arial", size=8))

        #limit number of x-axis ticks to prevent tick labels from overlapping
        maxNumTicks = 15
        xticks = ticker.MaxNLocator(min(maxNumTicks, len(x1)))
        axes[plotNum][0].xaxis.set_major_locator(xticks)

        #get test information to print
        axes[plotNum][1].text(0.0, 1.0, testName, verticalalignment="top", color="#012456", font="Arial", fontsize=12, weight="bold")
        axes[plotNum][1].text(0.0, 0.9, scenario, verticalalignment="top", color="#012456", font="Arial", fontsize=10)
        testText =  "\nLatest: " + "{:.3f}".format(latestRun)
        testText += "\nHistorical Baseline: "+ "{:.3f}".format(historicalBaselineScenario) + "\nChange from Historical Baseline: " + "{:.1f}".format(changeFromHistoricalBaseline) + "%"
        testText += "\nTest Baseline: "+ "{:.3f}".format(baselineScenario) + "\nChange from Test Baseline: " + "{:.1f}".format(changeFromBaseline) + "%"
        testText += "\nAverage: " + "{:.3f}".format(averages[scenario]) + "\nChange from Average: " + "{:.1f}".format(averageChange) + "%"
        axes[plotNum][1].text(0.0, 0.835, testText, verticalalignment="top", color="black", font="Arial", fontsize=10)

        # Print any bugs associated with the test
        testText = ''
        if testName in testBugs:
            lines = testBugs[testName][1:]
            if len(lines) >= 1:
                testText = "\nAssociated Bugs:\n"
            for line in lines:
                testText += line

        # Add suggestion if always above baseline
        allFailed = True
        for t in y1:
            if t <= baselineScenario:
                allFailed = False
        if allFailed:
            reccommendedBase = max(y1) * 1.1
            testText += "\nRecommendation: Update baseline to " + "{:.3f}".format(reccommendedBase) + ",\nor investigate performance.\n"

        # Add suggestion if newest data is more than two weeks old
        if lastDate[scenario] < datetime.today() - timedelta(14):
            testText += "\nRecommendation: Most recent data is old.\nCheck if the scenario has changed or has run.\n"
        
        axes[plotNum][1].text(0.0, 0.225, testText, verticalalignment="top", color = '#8d2424', font="Arial", fontsize=10, wrap=True)

        # start new page once all rows are populated
        if plotNum >= rows-1:
            pdf.savefig(fig)

            # formatting for report pages after first page
            fig = plt.figure(figsize=(11, 8.5), constrained_layout=False)
            gs = fig.add_gridspec(nrows=rows+2, ncols=columns+2, height_ratios=[0.5, 10, 10, 10, 0.45], width_ratios=[1, 20, 20, 1],
                left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.10, hspace=0.4)
            footer = fig.add_subplot(gs[-1, :])
            footer.get_xaxis().set_visible(False)
            footer.get_yaxis().set_visible(False)
            footer.set_facecolor('#012456')

            # creating subplots for pages after first page
            plotNum = 0
            axes = []
            for row in range(1, rows+1):
                axes.append([fig.add_subplot(gs[row, 1]), fig.add_subplot(gs[row, 2])])

            # hide axes in subplots that will be used for text entry
            for index in range(0, rows):
                axes[index][1].axis("off")

        else:
            plotNum += 1

#hide any empty plots that are created at the end of the pdf report
for index in range(plotNum, rows):
    axes[index][0].axis("off")

# save the last page of the report only if it is not blank
if plotNum != 0:
    pdf.savefig(fig)

# add message and save report if there are no failing scenarios
isFailures = False
for testname in results:
    if len(results[testname]) != 0:
        isFailures = True
        break
if not isFailures:
    axes[0][1].text(0.0, 1.0, "No performance scenarios flagged on {}.\nSee Power BI for detailed performance results.".format(str(datetime.today().strftime("%m/%d/%Y"))),
        verticalalignment="top", color="black", font="Arial", fontsize=12)
    pdf.savefig(fig)

pdf.close()