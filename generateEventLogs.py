import sys
import os
filePath = sys.argv[1]

pathForbaseline = filePath.replace("_duration.csv",".csv")

for i in range(1,9):
    for j in range(0,4):
        t = 0.1 - (0.025 * j)
        t = round(t,3)
        k = 2**i
        os.system("time python generate_baseline_log.py %s %s %s &" % (filePath,str(k),str(t)))
        #os.system("time python runPretsa.py %s %s %s &" % (filePath,str(k),t))