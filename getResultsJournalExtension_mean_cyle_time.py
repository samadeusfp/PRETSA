import pandas as pd
import os, sys
import statistics

def get_mean_cycle_times(filePath):
    eventLog = pd.read_csv(filePath, delimiter=";")
    mean_cycle_times = eventLog.groupby('Activity').Duration.agg("mean")
    return mean_cycle_times

dirPath = sys.argv[1]
dataset = sys.argv[2]
resultFilePath = os.path.join(dirPath, dataset + "_cycle_time_results.csv")

df = pd.DataFrame()

filePathOriginalLog = os.path.join(dirPath, dataset + "_dataset.csv")
original_cycle_time = get_mean_cycle_times(filePathOriginalLog)

for k in (4,8,16,32,64):
    for t in (1.0,2.0,3.0,4.0,5.0):
        for algorithm in ("pretsa","heuristic_pretsa","pretsa_star"):
            filePathAlgoLog = os.path.join(dirPath, dataset + "_dataset_t" + str(t) + "_k" + str(k) + "_" + algorithm + ".csv")
            data = dict()
            if os.path.exists(filePathAlgoLog):
                errors = list()
                log_cycle_times = get_mean_cycle_times(filePathAlgoLog)
                for activity in original_cycle_time.keys():
                    originalValue = original_cycle_time[activity]
                    if originalValue != 0.0:
                        algorithmValue = log_cycle_times.get(activity,0.0)
                        relativeError = abs((algorithmValue / originalValue) - 1.0)
                        if relativeError > 1:
                            relativeError = 1
                        errors.append(relativeError)
                data["k"] = k
                data["t"] = t
                data["algorithm"] = algorithm
                data["dataset"] = dataset
                data["error"] = statistics.mean(errors)
                df = df.append(data, ignore_index=True)
df.to_csv(resultFilePath)

