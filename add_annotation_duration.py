import sys
import csv
import datetime

class excel_semicolon(csv.excel):
    delimiter = ';'

dataset = sys.argv[1]
filePath = sys.argv[2]

caseIdColName = "Case ID"
durationColName = "Duration"

writeFilePath = filePath.replace(".csv","_duration.csv")
print(writeFilePath)

timeStampColName = "Complete Timestamp"


with open(filePath) as csvfile:
    with open(writeFilePath,'w') as writeFile:
        reader = csv.DictReader(csvfile,delimiter=";")
        fieldNamesWrite = reader.fieldnames
        fieldNamesWrite.append(durationColName)
        writer = csv.DictWriter(writeFile, fieldnames=fieldNamesWrite,dialect=excel_semicolon)
        writer.writeheader()
        currentCase = ""
        for row in reader:
            if dataset != "bpic2017":
                newTimeStamp = datetime.datetime.strptime(row[timeStampColName], '%Y/%m/%d %H:%M:%S.%f')
                if currentCase != row[caseIdColName]:
                    currentCase = row[caseIdColName]
                    duration = 0.0
                else:
                    duration = (newTimeStamp - oldTimeStamp).total_seconds()
                oldTimeStamp = newTimeStamp
            else:
                startTimeStamp = datetime.datetime.strptime(row[timeStampColName], '%Y/%m/%d %H:%M:%S.%f')
                endTimeStamp = datetime.datetime.strptime(row[timeStampColName], '%Y/%m/%d %H:%M:%S.%f')
                duration = (endTimeStamp - startTimeStamp).total_seconds()
            row[durationColName] = duration
            writer.writerow(row)