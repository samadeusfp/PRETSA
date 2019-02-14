import sys
import os

dictPath = sys.argv[1]

datasets = ["CoSeLoG", "Sepsis"]
for dataset in datasets:
    print(dataset)
    for k in range(1,9):
        k = 2**k
        filePath = dictPath + dataset + "_duration_pretsa_baseline_k" + str(k) + ".csv"
        os.system("time python add_annotation_duration.py normal %s" % (filePath))