import sys
import pandas as pd
import csv
import os
import numpy as np

class excel_semicolon(csv.excel):
    delimiter = ';'

dictPath = sys.argv[1]
writeFilePath = dictPath + "pretsa_statistics_annotations.csv"

with open(writeFilePath, 'w+') as writeFile:
    caseIDColName = "Case ID"
    datasets = ["Road_Traffic_Fine_Management_Process","CoSeLoG","Sepsis"]
    fieldNamesWrite = ["Event Log","k","t","method","activity","Avg. Duration"]
    writer = csv.DictWriter(writeFile, fieldnames=fieldNamesWrite, dialect=excel_semicolon)
    writer.writeheader()
    for dataset in datasets:
        for k in range(1,9):
            k = 2 ** k
            tString = ["0.1","0.07500000000000001","0.05","0.024999999999999994"]
            for t in range(0,4):
                filePath = dictPath + dataset + "_duration_t" + tString[t] + "_k" + str(k) + "_pretsa.csv"
                t = round(0.1 - (t*0.025), 3)
                if os.path.isfile(filePath):
                    eventLog = pd.read_csv(filePath, delimiter=";")
                    eventLog = eventLog.replace(-1.0,np.nan)
                    if not eventLog.empty:
                        data = eventLog.groupby('Activity').Duration.agg("mean")
                        for row in data.iteritems():
                            (key, value) = row
                            line = dict()
                            line["Event Log"] = dataset
                            line["k"] = k
                            line["t"] = str(t)
                            line["method"] = "pretsa"
                            line["activity"] = key
                            line["Avg. Duration"] = value
                            writer.writerow(line)
                else:
                    print(filePath + " does not exist")