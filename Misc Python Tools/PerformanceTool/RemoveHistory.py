import os
import sys

machines = [
    "CHQW10REG03",
    "chq2cjconnel1",
    "CHQW10REG01",
    "CHQW10REG02",
    "CHQ2COOP4393",
    "CHQ2DISCOTEST04"
    ]

# check if the number entered is an int
def isAnInt(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

# get scenario tag
tag = input("Enter tag of scenario you would like to modify: ").lower()

# get date
date = input("Enter the latest date you would like removed\nAll entries on and before this day will be deleted (mm/dd/yyyy): ")
day = 0
month = 0
year = 0
if date.count("/") == 2:
    splitDate = date.split("/")
    month = splitDate[0]
    day = splitDate[1]
    year = splitDate[2]
    if not isAnInt(day) or not isAnInt(month) or not isAnInt(year):
        print("Date entered contains invalid characters")
        sys.exit(1)
    day = int(day)
    month = int(month)
    year = int(year)
    if month > 12 or day > 31:
        print("Date entered is not valid")
        sys.exit(1)
else:
    print("Date entered contains invalid characters")
    sys.exit(1)

# iterate through list of machines
for machine in machines:
    perfPath = "\\\\{}\\PerformanceLogging".format(machine)
    # get all .log files
    files = os.listdir(perfPath)
    logs = []
    for f in files:
        if f.endswith(".log"):
            logs.append(perfPath + "\\" + f)

    # find .log file containing the tag
    found = False
    tagFile = ''
    for log in logs:
        if found:
            break
        with open(log, 'r') as file:
            lines = file.readlines()
            for line in lines:
                categories = line.split(", ")
                if categories[1].lower() == tag:
                    found = True
                    tagFile = log
                    print(tagFile)
                    break
    if not found:
        print("{}: Tag not found".format(machine))
        continue

    # load file into a list and remove unwanted lines
    lines = []
    with open(tagFile, 'r') as file:
        lines = file.readlines()
        for line in lines:
            categories = line.split(", ")
            tagDate = categories[0].split(" ")[0]
            splitTagDate = tagDate.split("/")
            tagDay = int(splitTagDate[1])
            tagMonth = int(splitTagDate[0])
            tagYear = int(splitTagDate[2])
            if tagYear < year and categories[1].lower() == tag:
                lines.remove(line)
            elif tagYear == year and tagMonth < month and categories[1].lower() == tag:
                lines.remove(line)
            elif tagYear == year and tagMonth == month and tagDay <= day and categories[1].lower() == tag:
                lines.remove(line)

    # write lines back to file after removing data
    try:
        with open(tagFile, 'w') as file:
            file.writelines(lines)
    except:
        print("ERROR: Directory is read-only. Cannot overwrite {}".format(tagFile))

    # remove csv file from directory
    csv = tagFile.split(".log")[0] + "_performance.csv"
    if os.path.exists(csv):
        try:
            os.remove(csv)
        except:
            print("ERROR: Directory is read-only. Cannot delete {}".format(csv))