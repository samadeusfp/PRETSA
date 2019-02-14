import sys
import pandas as pd
import numpy as np
filePath = sys.argv[1]

caseIDColName = "Case ID"
eventLog = pd.read_csv(filePath, delimiter=";")
number_variants = eventLog.Variant.value_counts()
traces = eventLog[caseIDColName].value_counts()

variants = eventLog.groupby('Variant')[caseIDColName].nunique(False)


print("Number of variants: " + str(number_variants.size))
print("Min cases for Variant: " + str(min(variants)))
print("Max cases for Variant: " + str(max(variants)))

print("Min events in case: " + str(min(traces)))
print("Max events in case: " + str(max(traces)))
print("Avg events in case: " + str(np.mean(traces)))

print(variants.sort_values())