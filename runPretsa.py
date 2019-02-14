import sys
from pretsa import Pretsa
import pandas as pd
import profile

filePath = sys.argv[1]
k = sys.argv[2]
t = sys.argv[3]
sys.setrecursionlimit(3000)
targetFilePath = filePath.replace(".csv","_t%s_k%s_pretsa.csv" % (t,k))


print("Load Event Log")
eventLog = pd.read_csv(filePath, delimiter=";")
print("Starting experiments")
pretsa = Pretsa(eventLog)
cutOutCases = pretsa.runPretsa(int(k),float(t))
print("Modified " + str(len(cutOutCases)) + " cases for k=" + str(k))
privateEventLog = pretsa.getPrivatisedEventLog()
privateEventLog.to_csv(targetFilePath, sep=";",index=False)