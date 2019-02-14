import sys
import pandas as pd
import numpy as np
dictPath = sys.argv[1]

caseIDColName = "Case ID"

datasets = ["Road_Traffic_Fine_Management_Process","CoSeLoG","Sepsis"]
df = pd.DataFrame(columns=['Dataset', 'k', 'method','variants','cases'])
for dataset in datasets:
    for k in range(1,9):
        k = 2**k
        filePath = dictPath + dataset + "_duration_pretsa_baseline_k" + str(k) + ".csv"
        eventLog = pd.read_csv(filePath, delimiter=";")
        number_variants = eventLog.Variant.value_counts()
        traces = eventLog[caseIDColName].value_counts()

        variants = eventLog.groupby('Variant')[caseIDColName].nunique(False)

        if len(traces) != 0:
            row = dict()
            row['Dataset'] = dataset
            row['k'] = k
            row['method'] = "baseline"
            row['variants'] = number_variants.size
            row['cases'] = len(traces)
            df = df.append(row,ignore_index=True)
            #print("Number of variants: " + str(number_variants.size))
            #print("Min cases for Variant: " + str(min(variants)))
            #print("Max cases for Variant: " + str(max(variants)))

            #print("Min events in case: " + str(min(traces)))
            #print("Max events in case: " + str(max(traces)))
            #print("Avg events in case: " + str(np.mean(traces)))
            #print(len(traces))

            #print(variants.sort_values())
csvPath = dictPath + "baseline_event_logs_statistics.csv"
df.to_csv(sep=";",path_or_buf=csvPath)