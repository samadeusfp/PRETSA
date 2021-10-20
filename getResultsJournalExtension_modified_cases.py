import os
import sys
import pickle
import pandas as pd

dirPath = sys.argv[1]
dataset = sys.argv[2]
resultFilePath = os.path.join(dirPath, dataset + "_modified_cases.csv")

df = pd.DataFrame()

for k in (4,8,16,32,64):
    for t in (1.0,2.0,3.0,4.0,5.0):
        for algorithm in  ("pretsa","heuristic_pretsa","pretsa_star"):
            filePath = os.path.join(dirPath,dataset+"_dataset_t"+str(t)+"_k"+str(k)+"_"+algorithm+".pickle")
            if os.path.exists(filePath):
                file = open(filePath, 'rb')
                data = pickle.load(file)
                file.close()
            else:
                data = dict()
                data["cases"] = -1
                data["inflictedChanges"] = -1
            if data["cases"] != -1:
                data["cases"] = len(data["cases"])
            data["k"] = k
            data["t"] = t
            data["algorithm"] = algorithm
            data["dataset"] = dataset
            df = df.append(data, ignore_index=True)
df.to_csv(resultFilePath)
