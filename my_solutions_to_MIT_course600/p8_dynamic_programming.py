# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#

import time

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    try:
        dict = {}
        inputFile = open(filename)
        for line in inputFile:
            name, value, work = line.strip().split(',')
            dict[name] = (int(value), int(work))
        return dict
    except IOError:
        raise ValueError("couldn't open " + filename)
        
def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

def testLoadSubjects():
    subjects = loadSubjects(SUBJECT_FILENAME)
    printSubjects(subjects)    
    
def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    assert type(subjects) == dict and maxWork > 0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    if comparator is cmpValue:
        subNames = sorted(subjects, key=lambda k: subjects[k][VALUE], 
                          reverse=True)
    if comparator is cmpWork:
        subNames = sorted(subjects, key=lambda k: subjects[k][WORK])
    if comparator is cmpRatio:
        subNames = sorted(subjects, 
                          key=lambda k: float(subjects[k][VALUE])/subjects[k][WORK], 
                          reverse=True)
    selected = {}
    i, totalVal, totalWork = 0, 0, 0
    while totalWork < maxWork and i < len(subNames):
        s = subNames[i]        
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        if totalWork + work <= maxWork:
            selected[s] = (val, work)
            totalWork += work
            totalVal += val
        i += 1
    return selected
    
def testGreedyAdvisor():
    smallCatalog = {'6.00': (16, 8),
                    '1.00': (7,  7),
                    '6.01': (5,  3),
                    '15.01': (9, 6)}
    print greedyAdvisor(smallCatalog, 15, cmpValue)
    print greedyAdvisor(smallCatalog, 15, cmpWork)
    selected = greedyAdvisor(smallCatalog, 15, cmpRatio)
    printSubjects(selected)
    subjects = loadSubjects(SUBJECT_FILENAME)
    selected = greedyAdvisor(subjects, 15, cmpValue)
    printSubjects(selected)
    selected = greedyAdvisor(subjects, 15, cmpWork)
    printSubjects(selected)
    selected = greedyAdvisor(subjects, 15, cmpRatio)
    printSubjects(selected)

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = subjects.keys()
    tupleList = subjects.values()
    bestSubset, bestSubsetValue = \
        bruteForceAdvisorHelper(subjects, nameList, maxWork, 0, None, None, 
                                [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, nameList, maxWork, i, bestSubset, 
                            bestSubsetValue, subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[nameList[i]]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = \
                bruteForceAdvisorHelper(subjects, nameList, maxWork, i+1, 
                                        bestSubset, bestSubsetValue, subset,
                                        subsetValue + s[VALUE], 
                                        subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(subjects, nameList, maxWork, i+1, 
                                    bestSubset, bestSubsetValue, subset,
                                    subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime():
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """
    subjects = loadSubjects(SUBJECT_FILENAME)
    maxWorks = [1, 5, 10, 15, 30, 45, 60, 75, 90, 105, 120]
    for maxWork in maxWorks:
        start = time.time()
        print bruteForceAdvisor(subjects, maxWork)
        end = time.time()
        print str(maxWork) + ': ' + str(end - start) + '\n'

# Problem 3 Observations
# ======================
#
# TODO: write here your observations regarding bruteForceTime's performance
# maxWork     time(secs)
# 1            0.004
# 5            0.432
# 10          74.219
# 15          too long

#
# Problem 4: Subject Selection By Dynamic Programming
#
def fastMaxVal(toConsider, tupleList, avail, memo = {}):
    # toConsider: a list of strings
    # tupleList: a list of (value, work) tuples
    # avail: available work
    # 
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif tupleList[0][WORK] > avail:
        result = fastMaxVal(toConsider[1:], tupleList[1:], avail, memo)
    else:
        s = toConsider[0]
        curr_work, curr_value = tupleList[0][WORK], tupleList[0][VALUE]
        withVal, withToTake = fastMaxVal(toConsider[1:], tupleList[1:], 
                                         avail - curr_work, memo)
        withVal += curr_value
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:], tupleList[1:], 
                                               avail, memo)
        if withVal > withoutVal:
            result = (withVal, withToTake + (s,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result

def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    result = {}
    nameList = subjects.keys()
    tupleList = subjects.values()
    totVal, selectedSubjects = fastMaxVal(nameList, tupleList, maxWork)
    for chosenSubject in selectedSubjects:
        result[chosenSubject] = subjects[chosenSubject]
    return result
    
def test_dpAdvisor():
    subjects = loadSubjects(SUBJECT_FILENAME)
    printSubjects(dpAdvisor(subjects, 30))

#
# Problem 5: Performance Comparison
#
def dpTime():
    """
    Runs tests on dpAdvisor and measures the time required to compute an
    answer.
    """
    subjects = loadSubjects(SUBJECT_FILENAME)
    maxWorks = [1, 5, 10, 15, 30, 45, 60, 75, 90, 105, 120]
    for maxWork in maxWorks:
        start = time.time()
        print dpAdvisor(subjects, maxWork)
        end = time.time()
        print str(maxWork) + ': ' + str(end - start) + '\n'


# Problem 5 Observations
# ======================
#
# TODO: write here your observations regarding dpAdvisor's performance and
# how its performance compares to that of bruteForceAdvisor.
# maxWork     time(secs)
# 1            0.005
# 5            0.044
# 10           0.052
# 15           0.055
# 30           0.100
# 45           0.104
# 60           0.115
# 75           0.118
# 90           0.122
# 105          0.129
# 120          0.144



if __name__ == "__main__":
    # testLoadSubjects()
    # testGreedyAdvisor()
    # bruteForceTime()
    # test_dpAdvisor()
    dpTime()
    