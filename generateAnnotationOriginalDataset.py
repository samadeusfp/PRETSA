import sys
import pandas as pd
import csv

class excel_semicolon(csv.excel):
    delimiter = ';'

dictPath = sys.argv[1]
writeFilePath = dictPath + "original_annotations_pretsa.csv"

with open(writeFilePath, 'w+') as writeFile:
    fieldNamesWrite = ["Event Log","method","activity","Avg. Duration"]
    writer = csv.DictWriter(writeFile, fieldnames=fieldNamesWrite, dialect=excel_semicolon)
    writer.writeheader()
    for dataset in ["CoSeLoG","Sepsis","Road_Traffic_Fine_Management_Process"]:
        filePath = dictPath + dataset + "_duration.csv"
        eventLog = pd.read_csv(filePath, delimiter=";")
        data = eventLog.groupby('Activity').Duration.agg("mean")
        for row in data.iteritems():
            (key, value) = row
            line = dict()
            line["Event Log"] = dataset
            line["method"] = "original"
            line["activity"] = key
            line["Avg. Duration"] = value
            writer.writerow(line)

