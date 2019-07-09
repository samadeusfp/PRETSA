# PRETSA
PRETSA (PREfix-Tree based event log SAnitisation for t-closeness) is an algorithm to generate privatizied event logs that comply with k-anonymity and t-closeness. These event logs can be used for process discovery a subfield of Process Mining. We provide an implementation of PRETSA in Python 3. Our code is available under the MIT license. If you use it for academic purposes please cite our paper:
```
@inproceedings{pretsaICPM2019,
    author  = "Stephan A. Fahrenkrog-Petersen and Han van der Aa and Matthias Weidlich",
    title   = "PRETSA: Event Log Sanitization for Privacy-aware Process Discovery",
    Booktitle = "1st IEEE International Conference on Process Mining",
    year    = "2019"
}
```
You can access the corresponding research paper here:
https://www.researchgate.net/publication/332173989_PRETSA_Event_Log_Sanitization_for_Privacy-aware_Process_Discovery


## Requirements
To run our algorithm you need the following Python packages:
- Pandas (https://pandas.pydata.org/index.html)
- SciPy (https://www.scipy.org)
- NumPy (http://www.numpy.org)
- AnyNode (https://anytree.readthedocs.io/en/latest/)

We did run our algorithm only with Python 3, so we can not guarantee that it works with Python 2.

## How to run PRETSA

The algorithm PRETSA itself is implemented in the file *pretsa.py*. To run the algorithm you first have to initiate the *Pretsa* class and hand over an event log represented as a pandas dataframe:
```
eventLog = pd.read_csv(filePath, delimiter=";")
pretsa = Pretsa(eventLog)
```
As a next step you run the PRETSA algorithm with your choosen k-anonymity(an integer) and t-closesness(a float) parameter. The algorithm then returns the cases that have been modified:
```
cutOutCases = pretsa.runPretsa(k,t)
```
Note that the privacy constraint k-anonymity gets stronger with a higher value, while t-closeness can have values between 1.0 and 0.0 with the lowest value giving the strongest privacy guarantee.

Finally we can return our privatizied event log as a pandas dataframe:
```
privateEventLog = pretsa.getPrivatisedEventLog()
```

Please consider that your original event log must contain at least the following attributes(column names), so that PRETSA can process it:
- Case Id
- Activity
- Duration

If you want to use different attribute column names you can change the following variables in *pretsa.py*:
- caseIDColName
- activityColName
- annotationColName

## How to repeat our experiments

We will describe in this section how we conducted our experiments for our ICPM 2019 submission:

First we generated the duration annotation with the following script:
```
python add_annotation_duration.py <fileName> <dataset>
```

Next by running the script *runPretsa.py* we generated the event log's generated by PRETSA with choosen parameters for *k* and *t*:
```
python runPretsa.py <fileName> <k> <t>
```
To generate privatizied event logs with our baseline approach we run the script *generate_baseline_log.py*:
```
python generate_baseline_log.py <fileName> <k> <t>
```

To compare the fitness and precision of the event logs we used ProM. The calculate the statistcs of event logs( e.g. number of variants in the log) we run the script *calculateDatasetStatistics.py*. Alternatively we can run the script *calculateBaselineStatistics.py* and *calculatePRETSAEventLogStatistics.py* to save the number of variants in the PRETSA/baseline event logs into a csv-file:
```
python calculateDatasetStatustics.py <fileName>
python calculatBaselineEventLogStatistics.py <dictName>
python calculatePRETSAEventLogStatistics.py <dictName>
```

To calculate the annotation error we did the scripts *calculateAnnotationsEventLog_baseline.py* and *calculateAnnotationsEventLog_pretsa.py* to calculate the average annotation for the privatizied event logs:
```
python calculateAnnotationsEventLog_baseline.py <dictName>
python calculateAnnotationsEventLog_pretsa.py <dictName>
```

With *generateAnnotationOriginalDataset.py* we generate the statistics of the original event logs:
```
python generateAnnotationOriginalDataset.py <dictName>
```

Finally we run *calculateAnnotationError.py* to calculate the relative error of the annotations for each activity:
```
python calculateAnnotationError.py <dictName>
```

## How to contact us
PRETSA was developed at the Process-driven Architecture group of Humboldt-Universität zu Berlin. If you want to contact us, just send us a mail at: fahrenks || hu-berlin.de
