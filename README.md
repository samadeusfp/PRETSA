# PRETSA-Algorithms Family

## Requirements
To run our algorithm you need the following Python packages:
- Pandas (https://pandas.pydata.org/index.html)
- SciPy (https://www.scipy.org)
- NumPy (http://www.numpy.org)
- AnyNode (https://anytree.readthedocs.io/en/latest/)

We did run our algorithm only with Python 3, so we can not guarantee that it works with Python 2.


## How to repeat our experiments


Please consider that your original event log must contain at least the following attributes(column names), so that PRETSA can process it:
- Case Id
- Activity
- Duration

If you want to use different attribute column names you can change the following variables in *pretsa.py*:
- caseIDColName
- activityColName
- annotationColName

We will describe in this section how we conducted our experiments for our journal submission:
```
python startExperimentsForJournalExtension_<algorithmName>.py <filePath>
```
That the parallel execution of all anonymization settings for the algorithm specified in <algorithmName>. Please note, that this starts 25 processes at the same time. All of them potentially need intensive computional resources. Therefore, we recommend only executing these scripts on a powerful server.
 
The evaluation metrics can be derived by running the the following scripts:
```
python getResultsJournalExtension_<evaluation_metric>.py <dirPath> <dataset> 
```
