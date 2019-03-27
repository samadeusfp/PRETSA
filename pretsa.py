from anytree import AnyNode, PreOrderIter
from levenshtein import levenshtein
import sys
from scipy.stats import wasserstein_distance
from scipy.stats import normaltest
import pandas as pd
import numpy as np

class Pretsa:
    def __init__(self,eventLog):
        root = AnyNode(id='Root', name="Root", cases=set(), sequence="", annotation=dict())
        current = root
        currentCase = ""
        traceToSequenceDict = dict()
        sequence = None
        self.caseIDColName = "Case ID"
        self.activityColName = "Activity"
        self.annotationColName = "Duration"
        self.constantEventNr = "Event_Nr"
        self.annotationDataOverAll = dict()
        self.normaltest_alpha = 0.05

        for index, row in eventLog.iterrows():
            activity = row[self.activityColName]
            annotation = row[self.annotationColName]
            if row[self.caseIDColName] != currentCase:
                if not sequence is None:
                    traceToSequenceDict[currentCase] = sequence
                currentCase = row[self.caseIDColName]
                current = root
                current.cases.add(currentCase)
                sequence = ""
            childAlreadyExists = False
            sequence = sequence + "@" + activity
            for child in current.children:
                if child.name == activity:
                    childAlreadyExists = True
                    current = child
            if not childAlreadyExists:
                node = AnyNode(id=index, name=activity, parent=current, cases=set(), sequence=sequence, annotations=dict())
                current = node
            current.cases.add(currentCase)
            current.annotations[currentCase] = annotation
            self.__addAnnotation(annotation, activity)
        #Handle last case
        traceToSequenceDict[currentCase] = sequence
        self.tree = root
        self.traceToSequenceDict = traceToSequenceDict
        self.numberOfTracesOriginal = len(self.tree.cases)
        self.sequentialPrunning = True
        self.__setMaxDifferences()


    def __addAnnotation(self, annotation, activity):
        dataForActivity = self.annotationDataOverAll.get(activity,None)
        if dataForActivity is None:
            self.annotationDataOverAll[activity] = []
            dataForActivity = self.annotationDataOverAll[activity]
        dataForActivity.append(annotation)

    def __setMaxDifferences(self):
        self.annotationMaxDifferences = dict()
        for key in self.annotationDataOverAll.keys():
            maxVal = max(self.annotationDataOverAll[key])
            minVal = min(self.annotationDataOverAll[key])
            self.annotationMaxDifferences[key] = abs(maxVal - minVal)

    def __violatesTCloseness(self, activity, annotations, t, cases):
        distributionActivity = self.annotationDataOverAll[activity]
        maxDifference = self.annotationMaxDifferences[activity]
        #Consider only data from cases still in node
        distributionEquivalenceClass = []
        casesInClass = cases.intersection(set(annotations.keys()))
        for caseInClass in casesInClass:
            distributionEquivalenceClass.append(annotations[caseInClass])
        if len(distributionEquivalenceClass) == 0: #No original annotation is left in the node
            return False
        if maxDifference == 0.0: #All annotations have the same value(most likely= 0.0)
            return False
        if (wasserstein_distance(distributionActivity,distributionEquivalenceClass)/maxDifference) >= t:
            return True
        else:
            return False

    def __treePrunning(self, k,t):
        cutOutTraces = set()
        for node in PreOrderIter(self.tree):
            if node != self.tree:
                node.cases = node.cases.difference(cutOutTraces)
                if len(node.cases) < k or self.__violatesTCloseness(node.name, node.annotations, t, node.cases):
                    cutOutTraces = cutOutTraces.union(node.cases)
                    current = node.parent
                    node.parent = None
                    while current != self.tree:
                        current.cases = current.cases.difference(cutOutTraces)
                        current = current.parent
                    if self.sequentialPrunning:
                        break
        return cutOutTraces

    def __getAllPotentialSequencesTree(self,tree, sequence):
        sequences = set()
        sumCasesChildren = 0
        for child in tree.children:
            sumCasesChildren = sumCasesChildren + len(child.cases)
            childSequence = sequence + "@" + child.name
            sequences = sequences.union(self.__getAllPotentialSequencesTree(child, childSequence))
        if len(tree.cases) > sumCasesChildren or sumCasesChildren == 0:
            sequences.add(sequence)
        return sequences

    def __addCaseToTree(self, trace, sequence):
        if trace != "":
            activities = sequence.split("@")
            currentNode = self.tree
            self.tree.cases.add(trace)
            for activity in activities:
                for child in currentNode.children:
                    if child.name == activity:
                        child.cases.add(trace)
                        currentNode = child
                        break

    def __combineTracesAndTree(self, traces):
        #We transform the set of sequences into a list and sort it, to discretize the behaviour of the algorithm
        sequencesTree = list(self.__getAllPotentialSequencesTree(self.tree,""))
        sequencesTree.sort()
        for trace in traces:
            bestSequence = ""
            lowestDistance = sys.maxsize
            traceSequence = self.traceToSequenceDict[trace]
            for treeSequence in sequencesTree:
                currentDistance = levenshtein(traceSequence, treeSequence)
                if currentDistance < lowestDistance:
                    bestSequence = treeSequence
                    lowestDistance = currentDistance
            self.__addCaseToTree(trace, bestSequence)


    def runPretsa(self,k,t):
        if self.sequentialPrunning:
            cutOutCases = set()
            cutOutCase = self.__treePrunning(k,t)
            while len(cutOutCase) > 0:
                self.__combineTracesAndTree(cutOutCase)
                cutOutCases = cutOutCases.union(cutOutCase)
                cutOutCase = self.__treePrunning(k,t)
        else:
            cutOutCases = self.__treePrunning(k,t)
            self.__combineTracesAndTree(cutOutCases)
        return cutOutCases

    def __generateNewAnnotation(self, activity):
        #normaltest works only with more than 8 samples
        if(len(self.annotationDataOverAll[activity])) >=8:
            stat, p = normaltest(self.annotationDataOverAll[activity])
        else:
            p = 1.0
        if p <= self.normaltest_alpha:
            mean = np.mean(self.annotationDataOverAll[activity])
            std = np.std(self.annotationDataOverAll[activity])
            randomValue = np.random.normal(mean, std)
        else:
            randomValue = np.random.choice(self.annotationDataOverAll[activity])
        return randomValue

    def getPrivatisedEventLog(self):
        eventLog = pd.DataFrame()
        events = []
        for node in PreOrderIter(self.tree):
            if node != self.tree:
                for case in node.cases:
                    event = dict()
                    event[self.activityColName] = node.name
                    event[self.caseIDColName] = case
                    event[self.annotationColName] = node.annotations.get(case,self.__generateNewAnnotation(node.name))
                    event[self.constantEventNr] = node.depth
                    events.append(event)
        eventLog = pd.DataFrame(events)
        if not eventLog.empty:
            eventLog = eventLog.sort_values(by=[self.caseIDColName,self.constantEventNr])
        return eventLog