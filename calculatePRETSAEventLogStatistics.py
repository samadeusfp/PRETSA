import sys
import pandas as pd
dictPath = sys.argv[1]

caseIDColName = "Case ID"

datasets = ["CoSeLoG", "Sepsis","Road_Traffic_Fine_Management_Process"]
df = pd.DataFrame(columns=['Dataset', 'k', 'method','variants','cases'])
for dataset in datasets:
    for k in range(1,9):
        k = 2**k
        filePath = dictPath + dataset + "_duration_t1.0_k" + str(k) + "_pretsa.csv"
        eventLog = pd.read_csv(filePath, delimiter=";")
        variants = set()
        caseId = ""
        sequence = ""
        for ind in eventLog.index:

            if eventLog[caseIDColName][ind] != caseId:
                variants.add(sequence)
                caseId = eventLog[caseIDColName][ind]
                sequence = ""
            sequence += eventLog["Activity"][ind] + "@"

        traces = eventLog[caseIDColName].value_counts()

        if len(traces) != 0:
            row = dict()
            row['Dataset'] = dataset
            row['k'] = k
            row['method'] = "pretsa"
            row['variants'] = len(variants)
            row['cases'] = len(traces)
            print(row)
            df = df.append(row,ignore_index=True)
            #print("Number of variants: " + str(number_variants.size))
            #print("Min cases for Variant: " + str(min(variants)))
            #print("Max cases for Variant: " + str(max(variants)))

            #print("Min events in case: " + str(min(traces)))
            #print("Max events in case: " + str(max(traces)))
            #print("Avg events in case: " + str(np.mean(traces)))
            #print(len(traces))

            #print(variants.sort_values())
csvPath = dictPath + "pretsa_event_logs_statistics.csv"
df.to_csv(sep=";",path_or_buf=csvPath)