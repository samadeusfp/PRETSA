import os
import sys
import pickle
import pandas as pd

dirPath = sys.argv[1]
dataset = sys.argv[2]
resultFilePath = os.path.join(dirPath, dataset + "_runtime_results.csv")

df = pd.DataFrame()
t = 1.0

for k in (4,8,16,32,64):
    for algorithm in  ("pretsa","heuristic_pretsa","pretsa_star"):
        filePath = os.path.join(dirPath,dataset+"_dataset_t"+str(t)+"_k"+str(k)+"_"+algorithm+".pickle")
        result = dict()
        if os.path.exists(filePath):
            file = open(filePath, 'rb')
            data = pickle.load(file)
            file.close()
        else:
            data = dict()
            data["time"] = -1
        if data["time"] != -1:
            result["time"] = data["time"]
        result["k"] = k
        result["t"] = t
        result["algorithm"] = algorithm
        result["dataset"] = dataset
        df = df.append(result, ignore_index=True)
df.to_csv(resultFilePath)
