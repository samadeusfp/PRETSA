import os
import sys
import pandas as pd
from countVariantsInLog import count_variants

dirPath = sys.argv[1]
dataset = sys.argv[2]
resultFilePath = os.path.join(dirPath, dataset + "_variant_results.csv")

df = pd.DataFrame()


for k in (4,8,16,32,64):
    for t in (1.0,2.0,3.0,4.0,5.0):
        for algorithm in ("pretsa","heuristic_pretsa","pretsa_star"):
            filePathAlgoLog = os.path.join(dirPath, dataset + "_dataset_t" + str(t) + "_k" + str(k) + "_" + algorithm + ".csv")
            data = dict()
            if os.path.exists(filePathAlgoLog):
                event_log = pd.read_csv(filePathAlgoLog, delimiter=";")
                data["variants"] = count_variants(event_log)
            else:
                data["variants"] = 0
            data["k"] = k
            data["t"] = t
            data["algorithm"] = algorithm
            data["dataset"] = dataset
            df = df.append(data, ignore_index=True)
df.to_csv(resultFilePath)
