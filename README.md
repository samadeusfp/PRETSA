# PRETSA
PRETSA is an algorithm to generate privatizied event logs that comply with k-anonymity and t-closeness. These event logs can be used for process disvovery a subfield of Process Mining. We provide an implementation of PRETSA in Python 3. Our code is available under the MIT license. If you use it for academic purposes please cite our paper:

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

## How to contact us
PRETSA was developed at the Process-driven Architecture group of Humbodlt-Universität of Berlin. For contact information see the following website:
https://www.informatik.hu-berlin.de/de/forschung/gebiete/pda
