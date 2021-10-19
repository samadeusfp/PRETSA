import pretsa
import os
import sys

filePath = sys.argv[1]

for k in (4,8,16,32,64):
    #for t in (1.0,2.0,3.0,4.0,5.0):
    t = 1.0
    os.system("timeout 1d time python runExperimentForJournalExtension_pretsa_star.py %s %s %s &" % (filePath,str(k),str(t)))