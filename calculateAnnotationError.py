import sys
import pandas as pd
import csv
from statistics import mean

class excel_semicolon(csv.excel):
    delimiter = ';'


dictPath = sys.argv[1]

dictFiles = {"baseline":"pretsa_baseline_statistics_annotations.csv","pretsa":"pretsa_statistics_annotations.csv"}
fileOriginalDataPath = dictPath + "original_annotations_pretsa.csv"



originalData = pd.read_csv(fileOriginalDataPath, delimiter=";")
originalDataDict = dict()
for index, row in originalData.iterrows():
    activityDict = originalDataDict.get(row["Event Log"],dict())
    activityDict[row["activity"]] = row["Avg. Duration"]
    originalDataDict[row["Event Log"]] = activityDict

writeFilePath = dictPath + "pretsa_annotation_errors.csv"


with open(writeFilePath, 'w+') as writeFile:
    fieldNamesWrite = ["Event Log","method","k","t","activity","Relative Error"]
    writer = csv.DictWriter(writeFile, fieldnames=fieldNamesWrite, dialect=excel_semicolon)
    writer.writeheader()
    for method in dictFiles.keys():
        filePath = dictPath + dictFiles[method]
        algorithmData = pd.read_csv(filePath, delimiter=";")
        for k in range(1,9):
            k = 2**k
            for t in range(0,4):
                t = round(0.1 - (t*0.025), 3)
                for dataset in ["Sepsis","CoSeLoG","Road_Traffic_Fine_Management_Process"]:
                    currentSlide = algorithmData.loc[(algorithmData["k"] == k) & (algorithmData["t"] == t) & (algorithmData["Event Log"] == dataset)]
                    currentSlideDict = dict()
                    for index, rowInSlide in currentSlide.iterrows():
                        currentSlideDict[rowInSlide["activity"]] = rowInSlide["Avg. Duration"]
                    errorList = []
                    for activity in originalDataDict[dataset].keys():
                        originalValue = originalDataDict[dataset][activity]
                        if originalValue != 0.0:
                            algorithmValue = currentSlideDict.get(activity,0.0)
                            relativeError = abs((algorithmValue/originalValue) - 1.0)
                            csvRow ={}
                            csvRow["Event Log"] = dataset
                            csvRow["method"] = method
                            csvRow["k"] = k
                            csvRow["t"] = t
                            csvRow["activity"] = activity
                            csvRow["Relative Error"] = relativeError
                            writer.writerow(csvRow)
                            errorList.append(relativeError)
                    csvRow = {}
                    csvRow["Event Log"] = dataset
                    csvRow["method"] = method
                    csvRow["k"] = k
                    csvRow["t"] = t
                    csvRow["activity"] = "Average Activites"
                    csvRow["Relative Error"] = mean(errorList)
                    writer.writerow(csvRow)










