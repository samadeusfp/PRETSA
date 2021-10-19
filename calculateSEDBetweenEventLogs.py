import argparse
import pandas as pd
from levenshtein import levenshtein

caseIDColName = "Case ID"
activityColName = "Activity"

def get_cases_dict(event_log):
    caseToSequenceDict = dict()
    currentCase = ""
    sequence = None
    for index, row in event_log.iterrows():
        if row[caseIDColName] != currentCase:
            if not sequence is None:
                caseToSequenceDict[currentCase] = sequence
            currentCase = row[caseIDColName]
            sequence = ""
        sequence = sequence + "@" + row[activityColName]
    caseToSequenceDict[currentCase] = sequence
    return caseToSequenceDict

def get_distance(variant1,variant2,distanceMatrix):
    if distanceMatrix.get(variant1,None) is not None:
        if distanceMatrix[variant1].get(variant2,None) is None:
            distanceMatrix[variant1][variant2] = levenshtein(variant1,variant2)
            if distanceMatrix.get(variant2,None) is None:
                distanceMatrix[variant2] = dict()
            distanceMatrix[variant2][variant1] = distanceMatrix[variant1][variant2]
    else:
        distanceMatrix[variant1] = dict()
        distanceMatrix[variant1][variant2] = levenshtein(variant1, variant2)
        if distanceMatrix.get(variant2,None) is None:
            distanceMatrix[variant2] = dict()
        distanceMatrix[variant2][variant1] = distanceMatrix[variant1][variant2]
    return distanceMatrix[variant1][variant2]


def get_sed_between_logs(event_log_original, path_algo_log,distanceMatrix=dict()):
    event_log2 = pd.read_csv(path_algo_log,delimiter=";")
    event_log1_dict = get_cases_dict(event_log_original)
    event_log2_dict = get_cases_dict(event_log2)
    string_edit_distance = 0
    for case in event_log1_dict.keys():
        if event_log2_dict.get(case,None) is not None:
            string_edit_distance = string_edit_distance + get_distance(event_log1_dict[case],event_log2_dict[case],distanceMatrix)
        else:
            string_edit_distance = string_edit_distance + event_log1_dict[case].count("@")
    print(string_edit_distance)
    return string_edit_distance