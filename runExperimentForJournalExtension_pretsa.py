import sys
from pretsa import Pretsa
import pandas as pd
import pickle
import time

filePath = sys.argv[1]
k = sys.argv[2]
t = sys.argv[3]
sys.setrecursionlimit(3000)
targetFilePath = filePath.replace(".csv","_t%s_k%s_pretsa.csv" % (t,k))

eventLog = pd.read_csv(filePath, delimiter=";")
start = time.time()
pretsa = Pretsa(eventLog)
cutOutCases, distanceLog = pretsa.runPretsa(int(k),float(t),normalTCloseness=False)

eventLog = pretsa.getPrivatisedEventLog()
eventLog.to_csv(targetFilePath,index=None,header=True,sep=';')
end = time.time()


targetFilePathPickle = filePath.replace(".csv","_t%s_k%s_pretsa.pickle" % (t,k))
pickle.dump({"cases": cutOutCases, "inflictedChanges":distanceLog,"time":(end-start)}, open(targetFilePathPickle, "wb" ))