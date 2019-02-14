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

filePath = sys.argv[1]
kString = sys.argv[2]
tString = sys.argv[3]

k = int(kString)
t = float(tString)

caseIdColName = "Case ID"
variantColName = "Variant"
activityColName = "Activity"

writeFilePath = filePath.replace(".csv","_pretsa_baseline_k%s_t%s.csv" % (kString,tString))

timeStampColName = "Complete Timestamp"

with open(filePath) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    variantsDict = {}
    variantsAnnotationDict = {}
    currentCase = ""
    eventsBefore = 0
    activityDistributions = {}
    for row in reader:
        eventsBefore += 1
        if currentCase != row[caseIdColName]:
            currentCase = row[caseIdColName]
            if row[variantColName] in variantsDict:
                variantCounter = variantsDict.get(row[variantColName])
            else:
                variantCounter = 0
            variantsDict[row[variantColName]] = variantCounter + 1
        currentActivity = row[activityColName]
        currentVariant = row[variantColName]
        duration = float(row["Duration"])
        if currentActivity in activityDistributions:
            activityDistributions[currentActivity].append(duration)
        else:
            activityDistributions[currentActivity] = [duration]
        if row[variantColName] in variantsAnnotationDict:
            variantDistributions = variantsAnnotationDict.get(currentVariant)
        else:
            variantDistributions = {}
        if currentActivity in variantDistributions:
            variantDistributions[currentActivity].append(duration)
        else:
            variantDistributions[currentActivity] = [duration]
        variantsAnnotationDict[currentVariant] = variantDistributions

    variantsViolatingTcloseness = set()

    for variant in variantsAnnotationDict.keys():
        for activity in variantsAnnotationDict[variant].keys():
            if violatesTCloseness(activityDistributions[activity],variantsAnnotationDict[variant][activity],t):
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
            if variantsDict[row[variantColName]] >= k:
                eventsAfter += 1
                writer.writerow(row)
print("Events before " + str(eventsBefore))
print("Events after " + str(eventsAfter))
print("Remaining " + str(eventsAfter/eventsBefore))