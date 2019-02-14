import sys
import csv
import datetime
from scipy.stats import wasserstein_distance

class excel_semicolon(csv.excel):
    delimiter = ';'

def violatesTCloseness(distributionActivity, distributionEquivalenceClass, t):
    maxDifference = max(distributionActivity) - min(distributionActivity)
    if maxDifference == 0.0: #All annotations have the same value(most likely= 0.0)
        return False
    if (wasserstein_distance(distributionActivity,distributionEquivalenceClass)/maxDifference) >= t:
        return True
    else:
        return False

genericFilePath = sys.argv[1]
tString = sys.argv[2]

t = float(tString)

caseIdColName = "Case ID"
variantColName = "Variant"
activityColName = "Activity"

for k in range(8,9):
    k = 2**k
    kString = str(k)
    filePath = genericFilePath + kString + "_duration.csv"
    writeFilePath = filePath.replace("_duration_pretsa_baseline_k%s_duration.csv" % kString,"_duration_pretsa_baseline_k%s_t%s.csv" % (kString,str(t)))
    timeStampColName = "Complete Timestamp"
    activityDistributions = {}
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        variantsDict = {}
        currentCase = ""
        eventsBefore = 0
        for row in reader:
            eventsBefore += 1
            currentCase = row[caseIdColName]
            currentActivity = row[activityColName]
            currentVariant = row[variantColName]
            duration = float(row["Duration"])
            if currentActivity in activityDistributions:
                activityDistributions[currentActivity].append(duration)
            else:
                activityDistributions[currentActivity] = [duration]
            if row[variantColName] in variantsDict:
                variantDistributions = variantsDict.get(currentVariant)
            else:
                variantDistributions = {}
            if currentActivity in variantDistributions:
                variantDistributions[currentActivity].append(duration)
            else:
                variantDistributions[currentActivity] = [duration]
            variantsDict[currentVariant] = variantDistributions


    variantsViolatingTcloseness = set()

    for variant in variantsDict.keys():
        for activity in variantsDict[variant].keys():
            if violatesTCloseness(activityDistributions[activity],variantsDict[variant][activity],t):
                variantsViolatingTcloseness.add(variant)



    with open(filePath) as csvfile:
        with open(writeFilePath,'w') as writeFile:
            reader = csv.DictReader(csvfile,delimiter=";")
            fieldNamesWrite = reader.fieldnames
            writer = csv.DictWriter(writeFile, fieldnames=fieldNamesWrite,dialect=excel_semicolon)
            writer.writeheader()
            eventsAfter = 0
            next(reader)
            for row in reader:
                if not row[variantColName] in variantsViolatingTcloseness:
                    eventsAfter += 1
                    writer.writerow(row)
    print("Events before " + str(eventsBefore))
    print("Events after " + str(eventsAfter))
    print("Remaining " + str(eventsAfter/eventsBefore))